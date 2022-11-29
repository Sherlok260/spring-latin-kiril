package com.example.springlatinkirildemo3.service;

import com.example.springlatinkirildemo3.payload.ApiResponse;
import org.docx4j.XmlUtils;
import org.docx4j.openpackaging.exceptions.Docx4JException;
import org.docx4j.openpackaging.packages.WordprocessingMLPackage;
import org.docx4j.openpackaging.parts.WordprocessingML.MainDocumentPart;
import org.docx4j.openpackaging.parts.relationships.Namespaces;
import org.docx4j.openpackaging.parts.relationships.RelationshipsPart;
import org.docx4j.relationships.Relationship;
import org.python.core.PyObject;
import org.python.util.PythonInterpreter;
import org.springframework.web.multipart.MultipartFile;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.bind.JAXBException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import static org.python.core.io.IOBase.DEFAULT_BUFFER_SIZE;

@org.springframework.stereotype.Service
public class Service {
    public ApiResponse function(MultipartFile request) throws IOException, ParserConfigurationException, SAXException, TransformerException, Docx4JException, JAXBException {
        MultipartFile filee = request;

//        assert filee != null;

        FileOutputStream fileOutputStream = new FileOutputStream(filee.getOriginalFilename());
        fileOutputStream.write(filee.getBytes());
        fileOutputStream.close();

        System.out.println(filee.getOriginalFilename());

        String pathDocxFile = filee.getOriginalFilename();
//        String pathDocxFile = "MK_2_amaliy.docx";

        File docx = new File(pathDocxFile);
        ZipFile zipFile = new ZipFile(docx);
        ZipEntry zipEntry = zipFile.getEntry("word/document.xml");

        byte[] bytes = new byte[DEFAULT_BUFFER_SIZE];

        InputStream inputStream = zipFile.getInputStream(zipEntry);

        File file = new File("default.xml");

        FileOutputStream outputStream = new FileOutputStream(file, false);
        int read;

        while ((read = inputStream.read(bytes)) != -1) {
            outputStream.write(bytes, 0, read);
        }

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();

        Document xml = builder.parse(new File("default.xml"));
        NodeList employeeElements = xml.getDocumentElement().getElementsByTagName("w:t");

        PythonInterpreter pythonInterpreter = new PythonInterpreter();
        pythonInterpreter.execfile("translate.py");
        inputStream.close();

        for (int i = 0; i < employeeElements.getLength(); i++) {

            try {
                PyObject latin_to_kril = pythonInterpreter.eval("to_cyrillic('"+employeeElements.item(i).getTextContent()+"')");

                if(latin_to_kril.toString().equals(" ")) {
                    continue;
                }

                String response_latin_to_kril = latin_to_kril.toString();
                byte bytess[] = response_latin_to_kril.getBytes("ISO-8859-1");
                String result_latin_to_kril = new String(bytess, "UTF-8");

                xml.getDocumentElement().getElementsByTagName("w:t").item(i).setTextContent(result_latin_to_kril);

            } catch (Exception e) {
                System.out.println("xatolik: " + employeeElements.item(i).getTextContent());
            }
        }

        TransformerFactory transformerFactory =
                TransformerFactory.newInstance();
        Transformer transformer=
                transformerFactory.newTransformer();
        DOMSource source = new DOMSource(xml);
        StreamResult result=new StreamResult(new File("document.xml"));
        transformer.transform(source, result);

        WordprocessingMLPackage wordMLPackage = WordprocessingMLPackage.load(new File(pathDocxFile));

        RelationshipsPart relationshipsPart = wordMLPackage.getMainDocumentPart().getRelationshipsPart();

        Relationship sourceRelationship = wordMLPackage.getMainDocumentPart().getSourceRelationship();

        MainDocumentPart mainDocumentPart = new MainDocumentPart();

        wordMLPackage.getParts().put(mainDocumentPart);
        mainDocumentPart.setPackage(wordMLPackage);

        wordMLPackage.setPartShortcut(mainDocumentPart, Namespaces.DOCUMENT);

        mainDocumentPart.setSourceRelationship(sourceRelationship);
        mainDocumentPart.setRelationships(relationshipsPart);

        BufferedReader in = new BufferedReader(new FileReader("document.xml"));
        StringBuffer output = new StringBuffer();
        String st;
        while((st=in.readLine()) != null) {
            output.append(st);
        }

        mainDocumentPart.setJaxbElement((org.docx4j.wml.Document) XmlUtils.unmarshalString(output.toString()));
        wordMLPackage.save(new File("Result.docx"));

        in.close();
        outputStream.close();
        zipFile.close();
        new File(filee.getOriginalFilename()).delete();

        return new ApiResponse("success", true);
    }
}
