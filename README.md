# Covid_EndToEnd_Pipeline
(Work in progress) Data Engineering Project with Airflow, Snowflake, Tableau, and scripting in Shell and Python

The final state of the project will be an ELT pipeline orchestrated with Apache Airflow which downloads raw economic data from API's, loads the raw data into snowflake, transforms it in snowflake (e.g. clean, merge, and/or aggregate), exports the transformed data to local storage which will be connected to a Tableau dashboard. The data will refresh daily and tasks will also include clean up and archiving of files used in the ELT process.
