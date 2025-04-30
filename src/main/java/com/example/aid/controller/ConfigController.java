package com.example.aid.controller;

import com.example.aid.entity.Config;
import com.example.aid.service.ConfigService;
import jakarta.servlet.http.HttpSession;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.List;

@Controller
@AllArgsConstructor
public class ConfigController {

    private final ConfigService configService;
    
    @GetMapping("config")
    public String showConfig(Model model, HttpSession session) {
        List<Config> configList = configService.getAllActivatedConfigs();
        model.addAttribute("configList", configList);
        return "config";
    }

    @PostMapping("/config/update")
        public String updateConfig(@ModelAttribute Config config) {
        configService.saveConfig(config);
        return "redirect:/config";
    }
}
