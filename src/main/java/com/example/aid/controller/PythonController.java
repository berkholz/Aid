package com.example.aid.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class PythonController {

    private static final String SETTINGS_FILE_PATH = "/python/settings.py";

    @PostMapping("/update-download-path")
    public ResponseEntity<String> updateDownloadPath(@RequestParam String newPath) {
        try {
            List<String> lines = Files.readAllLines(Paths.get(SETTINGS_FILE_PATH));
            for (int i = 0; i < lines.size(); i++) {
                if (lines.get(i).startsWith("DOWNLOAD_PATH")) {
                    lines.set(i, "DOWNLOAD_PATH = \"" + newPath + "\"");
                    break;
                }
            }
            Files.write(Paths.get(SETTINGS_FILE_PATH), lines);
            return ResponseEntity.ok("DOWNLOAD_PATH updated successfully.");
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error updating DOWNLOAD_PATH.");
        }
    }
}