package com.example.aid.service;


import com.example.aid.entity.Config;
import com.example.aid.repository.ConfigRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@AllArgsConstructor
@Service
public class ConfigService {
    private final ConfigRepository configRepository;

    public Config getConfigByAppName(String appName) {
        return configRepository.findByAppName(appName);
    }

    public List<Config> getConfigs() {
        return (List<Config>) configRepository.findAll();
    }

    public List<Config> getActivatedConfigs() {
        return configRepository.findByActivated(true);
    }

    public List<Config> getDeactivatedConfigs() {
        return configRepository.findByActivated(false);
    }

    public void updateConfig(Config config) {
        Config existingConfig = configRepository.findById(config.getId()).orElse(null);


    }

    public void saveConfig(Config config) {
        configRepository.save(config);
    }

    public void deleteConfig(Long id) {
        configRepository.deleteById(id);
    }
}
