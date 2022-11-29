package com.example.springlatinkirildemo3.controller;

import com.example.springlatinkirildemo3.payload.ApiResponse;
import com.example.springlatinkirildemo3.service.Service;
import org.docx4j.openpackaging.exceptions.Docx4JException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.util.ResourceUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.xml.sax.SAXException;

import javax.xml.bind.JAXBException;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerException;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

@RestController
@RequestMapping("api")
//@CrossOrigin(origins = )
public class Controller {

    @Autowired
    private Service service;

    @PostMapping(value = "/file")
    public HttpEntity<?> saveFile(@RequestParam("file") MultipartFile request) throws IOException, ParserConfigurationException, SAXException, Docx4JException, JAXBException, TransformerException {

        ApiResponse function = service.function(request);

        return ResponseEntity.ok(function.getMessage());

    }

    @GetMapping("/hello")
    public HttpEntity<?> hello() {
        return ResponseEntity.ok("Hello");
    }

    @GetMapping("/hello2")
    public HttpEntity<?> hello2() {
        return ResponseEntity.ok("Hello Nima gape");
    }

    @GetMapping(value = "/getfile", produces = { "application/octet-stream" })
    public ResponseEntity<byte[]> download() {

        try {

            File file = ResourceUtils.getFile("Result.docx");

            byte[] contents = Files.readAllBytes(Paths.get(file.getAbsolutePath()));

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
            headers.setContentDisposition(ContentDisposition.attachment().filename("Result.docx").build());

            return new ResponseEntity<>(contents, headers, HttpStatus.OK);
        } catch (Exception e) {
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }


    /*
    FROM openjdk:17
EXPOSE 8080
ADD target/spring-boot-docker-demo.jar spring-boot-docker-demo.jar
ENTRYPOINT ["java", "-jar", "/spring-boot-docker-demo.jar"]
    * */

}
