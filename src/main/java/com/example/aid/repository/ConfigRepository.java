package com.example.aid.repository;

import com.example.aid.entity.Config;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.RepositoryDefinition;
import java.util.List;

@RepositoryDefinition(domainClass = ConfigRepository.class, idClass = Long.class)
public interface ConfigRepository extends CrudRepository<Config, Long> {
    Config findByAppName(String appName);
    List<Config> findByActivated(boolean activated);
}
