package com.example.aid.controller;

import com.example.aid.service.ModuleService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@AllArgsConstructor
@Controller
public class DashboardController {

    private final ModuleService moduleService;

    @GetMapping({"/dashboard", "/"})
    public String showDashboard() {
        return "dashboard";
    }

    @GetMapping("/documentation")
    public String showDocumentation() {
        return "documentation";
    }
}
