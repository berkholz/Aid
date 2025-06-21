package com.example.aid.repository;

import com.example.aid.entity.Module;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.RepositoryDefinition;
import java.util.List;

@RepositoryDefinition(domainClass = ModuleRepository.class, idClass = Long.class)
public interface ModuleRepository extends CrudRepository<Module, Long> {
    Module findByAppName(String appName);
    List<Module> findByActivated(boolean activated);
}
