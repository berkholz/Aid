package com.example.aid.service;


import com.example.aid.entity.Module;
import com.example.aid.repository.ModuleRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@AllArgsConstructor
@Service
public class ModuleService {
    private final ModuleRepository moduleRepository;

    public Module getModuleByAppName(String appName) {
        return moduleRepository.findByAppName(appName);
    }

    public List<Module> getModules() {
        return (List<Module>) moduleRepository.findAll();
    }

    public List<Module> getActivatedModules() {
        return moduleRepository.findByActivated(true);
    }

    public List<Module> getDeactivatedModules() {
        return moduleRepository.findByActivated(false);
    }

    public void saveModule(Module module) {
        moduleRepository.save(module);
    }

    // May not be needed
    public void deleteModule(Long id) {
        moduleRepository.deleteById(id);
    }
}
