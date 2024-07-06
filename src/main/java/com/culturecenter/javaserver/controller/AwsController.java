package com.culturecenter.javaserver.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class AwsController {
    @RequestMapping(value = "/health/check", method = {RequestMethod.GET, RequestMethod.POST})
    public ResponseEntity<Boolean> healthCheck(){
        return ResponseEntity.ok().body(true);
    }
}
