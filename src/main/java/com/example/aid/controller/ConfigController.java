package com.example.aid.controller;

import com.example.aid.entity.Config;
import com.example.aid.service.ConfigService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

@Controller
@AllArgsConstructor
public class ConfigController {

    private final ConfigService configService;
    
    @GetMapping("config")
    public String showConfig(
            @RequestParam(value = "order", required = false, defaultValue = "asc") String order,
            @RequestParam(value = "filter", required = false, defaultValue = "all") String filter,
            Model model) {
        List<Config> configList;

        if (filter != null && filter.equals("activated")) {
            configList = configService.getActivatedConfigs();
        } else if (filter != null && filter.equals("deactivated")) {
            configList = configService.getDeactivatedConfigs();
        } else {
            configList = configService.getConfigs();
        }

        if (order.equals("desc")) {
            configList.sort((c1, c2) -> c2.getAppName().compareTo(c1.getAppName())); order = "desc";
        } else if (order.equals("asc")) {
            configList.sort((c1, c2) -> c1.getAppName().compareTo(c2.getAppName())); order = "asc";
        }

        model.addAttribute("order", order);
        model.addAttribute("filter", filter);
        model.addAttribute("configList", configList);
        return "config";
    }

    @PostMapping("/config/update")
        public String updateConfig(@ModelAttribute Config config, RedirectAttributes redirectAttributes) {
        configService.saveConfig(config);
        redirectAttributes.addFlashAttribute("msg", "Konfiguration erfolgreich aktualisiert");
        return "redirect:/config";
    }
}
