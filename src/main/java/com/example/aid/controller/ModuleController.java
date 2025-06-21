package com.example.aid.controller;

import com.example.aid.entity.Module;
import com.example.aid.service.ModuleService;
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
public class ModuleController {

    private final ModuleService moduleService;
    
    @GetMapping("module")
    public String showModule(
            @RequestParam(value = "order", required = false, defaultValue = "asc") String order,
            @RequestParam(value = "filter", required = false, defaultValue = "all") String filter,
            Model model) {
        List<Module> moduleList;

        if (filter != null && filter.equals("activated")) {
            moduleList = moduleService.getActivatedModules();
        } else if (filter != null && filter.equals("deactivated")) {
            moduleList = moduleService.getDeactivatedModules();
        } else {
            moduleList = moduleService.getModules();
        }

        if (order.equals("desc")) {
            moduleList.sort((c1, c2) -> c2.getAppName().compareTo(c1.getAppName())); order = "desc";
        } else if (order.equals("asc")) {
            moduleList.sort((c1, c2) -> c1.getAppName().compareTo(c2.getAppName())); order = "asc";
        }

        model.addAttribute("order", order);
        model.addAttribute("filter", filter);
        model.addAttribute("moduleList", moduleList);
        return "module";
    }

    @PostMapping("/module/update")
    public String updateModule(@ModelAttribute("moduleList") List<Module> moduleList, RedirectAttributes redirectAttributes) {
        try {
        moduleList.forEach(moduleService::saveModule);
        redirectAttributes.addFlashAttribute("msg", "Changes saved!");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", e.getMessage());
        }
        return "redirect:/module";
    }
}
