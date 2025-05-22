package com.example.aid.controller;


import lombok.AllArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@AllArgsConstructor
public class ApplicationController {

    @GetMapping("/applications")
    public String showApplication() {
        return "applications";
    }
}
