package com.example.aid.controller;

import com.example.aid.service.ConfigService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@AllArgsConstructor
@Controller
public class DashboardController {

    private final ConfigService configService;

    @GetMapping({"/dashboard", "/"})
    public String showDashboard() {
        return "dashboard";
    }

    @GetMapping("/documentation")
    public String showDocumentation() {
        return "documentation";
    }
}
