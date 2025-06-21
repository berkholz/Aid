
CREATE TABLE module
(
    id        BIGINT GENERATED ALWAYS AS IDENTITY,
    app_name  VARCHAR(255),
    activated BOOLEAN NOT NULL
);

-- Data for Module table
INSERT INTO module (app_name, activated) VALUES ('7zip', TRUE);
INSERT INTO module (app_name, activated) VALUES ('adobe', TRUE);
INSERT INTO module (app_name, activated) VALUES ('adobe_enterprise', TRUE);
INSERT INTO module (app_name, activated) VALUES ('firefox_esr', TRUE);
INSERT INTO module (app_name, activated) VALUES ('gimp', TRUE);
INSERT INTO module (app_name, activated) VALUES ('inkscape', TRUE);
INSERT INTO module (app_name, activated) VALUES ('keepass', TRUE);
INSERT INTO module (app_name, activated) VALUES ('ms_powerbi_desktop', TRUE);
INSERT INTO module (app_name, activated) VALUES ('ms_powerbi_report_server', TRUE);
INSERT INTO module (app_name, activated) VALUES ('notepadpp', TRUE);
INSERT INTO module (app_name, activated) VALUES ('putty', TRUE);
INSERT INTO module (app_name, activated) VALUES ('sysinternal_utilities', TRUE);
INSERT INTO module (app_name, activated) VALUES ('sqldeveloper', TRUE);
INSERT INTO module (app_name, activated) VALUES ('sqlitebrowser', TRUE);
INSERT INTO module (app_name, activated) VALUES ('stunnel', TRUE);
INSERT INTO module (app_name, activated) VALUES ('winscp', TRUE);

