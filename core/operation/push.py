from core.configuration.variables import PathConf, GitlabEnvConf
from core.operation.command import Command
from os import system, path, chdir, getcwd, rename, remove

class GitPushOps():
    cmd              = Command()
    path             = PathConf()
    gitlab_env       = GitlabEnvConf()

    def push_to_code(self):
        chdir(self.path.code_path)
        for branch in self.gitlab_env.branches:
            system('git checkout -b' + branch)
            if branch == "develop":
                self.cmd.file_copy(self.path.gitlab_ci_source_path, self.path.gitlab_ci_destination_path)
                if self.gitlab_env.CI_PROJECT_GENERATION == "TRUE" and self.gitlab_env.CI_PROJECT_TYPE_BACKEND == "TRUE" and self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE":
                    self.cmd.recursive_copy(self.path.project_gradle_multi_module_source_path, self.path.project_destination_folder)
                    self.cmd.replacement(self.path.gradle_settings,'__CD_HELM_CHART_NAME__', self.gitlab_env.CI_PROJECT_NAME)
                elif self.gitlab_env.CI_PROJECT_GENERATION == "TRUE" and self.gitlab_env.CI_PROJECT_TYPE_BACKEND == "TRUE" and self.gitlab_env.CI_PROJECT_MODE_MONO_REPO == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE":
                    self.cmd.recursive_copy(self.path.project_gradle_single_module_source_path, self.path.project_destination_folder)
                    print(self.path.project_gradle_single_module_source_path)
                    print(self.path.project_destination_folder)
                    self.cmd.replacement(self.path.gradle_settings,'__CD_HELM_CHART_NAME__', self.gitlab_env.CI_PROJECT_NAME)
                    self.cmd.replacement(self.path.gradle_application_yaml,'__CD_HELM_CONTAINER_PORT__', self.gitlab_env.CD_HELM_CONTAINER_PORT)
                    self.cmd.replacement(self.path.gradle_application_yaml,'__CD_HELM_MANAGEMENT_PORT__', self.gitlab_env.CD_HELM_MANAGEMENT_PORT)
                
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TYPE_FRONTEND__', self.gitlab_env.CI_PROJECT_TYPE_FRONTEND)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TYPE_BACKEND__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TYPE_BACKEND_DMZ__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_MODE_MONO_REPO__', self.gitlab_env.CI_PROJECT_MODE_MONO_REPO)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_MODE_MULTI_MODULE__', self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_APPLICATION_TYPE_MAVEN__', self.gitlab_env.CI_APPLICATION_TYPE_MAVEN)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_APPLICATION_TYPE_GRADLE__', self.gitlab_env.CI_APPLICATION_TYPE_GRADLE )
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_APPLICATION_TYPE_PYTHON__', self.gitlab_env.CI_APPLICATION_TYPE_PYTHON )
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_RELEASE_TYPE_JIB__', self.gitlab_env.CI_RELEASE_TYPE_JIB)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_RELEASE_TYPE_KANIKO__', self.gitlab_env.CI_RELEASE_TYPE_KANIKO)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_CODE_STYLE_SONARQUBE__', self.gitlab_env.CI_CODE_STYLE_SONARQUBE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_CODE_CHECK_SNYK__', self.gitlab_env.CI_CODE_CHECK_SNYK)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TEST_STAGE__', self.gitlab_env.CI_PROJECT_TEST_STAGE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_BACKEND_IMAGE_VERSION_GRADLE__', self.gitlab_env.CI_BACKEND_IMAGE_VERSION_GRADLE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_BACKEND_IMAGE_VERSION_MAWEN__', self.gitlab_env.CI_BACKEND_IMAGE_VERSION_MAWEN)
            elif branch == "master":
                self.cmd.file_copy(self.path.gitlab_ci_source_path, self.path.gitlab_ci_destination_path)
                if self.gitlab_env.CI_PROJECT_GENERATION == "TRUE" and self.gitlab_env.CI_PROJECT_TYPE_BACKEND == "TRUE" and self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE":
                    self.cmd.recursive_copy(self.path.project_gradle_multi_module_source_path, self.path.project_destination_folder)
                    self.cmd.replacement(self.path.gradle_settings,'__CD_HELM_CHART_NAME__', self.gitlab_env.CI_PROJECT_NAME)
                elif self.gitlab_env.CI_PROJECT_GENERATION == "TRUE" and self.gitlab_env.CI_PROJECT_TYPE_BACKEND == "TRUE" and self.gitlab_env.CI_PROJECT_MODE_MONO_REPO == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE":
                    self.cmd.recursive_copy(self.path.project_gradle_single_module_source_path, self.path.project_destination_folder)
                    self.cmd.replacement(self.path.gradle_settings,'__CD_HELM_CHART_NAME__', self.gitlab_env.CI_PROJECT_NAME)
                    self.cmd.replacement(self.path.gradle_application_yaml,'__CD_HELM_CONTAINER_PORT__', self.gitlab_env.CD_HELM_CONTAINER_PORT)
                    self.cmd.replacement(self.path.gradle_application_yaml,'__CD_HELM_MANAGEMENT_PORT__', self.gitlab_env.CD_HELM_MANAGEMENT_PORT)
                
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TYPE_FRONTEND__', self.gitlab_env.CI_PROJECT_TYPE_FRONTEND)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TYPE_BACKEND__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TYPE_BACKEND_DMZ__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_MODE_MONO_REPO__', self.gitlab_env.CI_PROJECT_MODE_MONO_REPO)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_MODE_MULTI_MODULE__', self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_APPLICATION_TYPE_MAVEN__', self.gitlab_env.CI_APPLICATION_TYPE_MAVEN)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_APPLICATION_TYPE_GRADLE__', self.gitlab_env.CI_APPLICATION_TYPE_GRADLE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_APPLICATION_TYPE_PYTHON__', self.gitlab_env.CI_APPLICATION_TYPE_PYTHON)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_RELEASE_TYPE_JIB__', self.gitlab_env.CI_RELEASE_TYPE_JIB)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_RELEASE_TYPE_KANIKO__', self.gitlab_env.CI_RELEASE_TYPE_KANIKO)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_CODE_STYLE_SONARQUBE__', self.gitlab_env.CI_CODE_STYLE_SONARQUBE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_CODE_CHECK_SNYK__', self.gitlab_env.CI_CODE_CHECK_SNYK)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_PROJECT_TEST_STAGE__', self.gitlab_env.CI_PROJECT_TEST_STAGE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_BACKEND_IMAGE_VERSION_GRADLE__', self.gitlab_env.CI_BACKEND_IMAGE_VERSION_GRADLE)
                self.cmd.replacement(self.path.gitlab_ci_yaml,'__CI_BACKEND_IMAGE_VERSION_MAWEN__', self.gitlab_env.CI_BACKEND_IMAGE_VERSION_MAWEN)
            
            system('git add .')
            system("git status")
            system("git commit -am 'Configured project'")
            system("git push --set-upstream origin " + branch)
              
        path_parent = path.dirname(getcwd())
        chdir(path_parent)

    def push_to_chart(self):
        MODULE = ""
        if self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE != "NULL":
            MODULE = self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE
        else:
            MODULE = self.gitlab_env.CI_PROJECT_NAME
        chdir(self.path.chart_path)
        for branch in self.gitlab_env.branches:
            system('git checkout -b' + branch)
            if branch == "develop":
                self.cmd.recursive_copy(self.path.helm_chart_source_path, self.path.helm_chart_destination_path)
                rename(self.path.helm_chart_destination_path + 'values.yaml', self.path.helm_chart_destination_path + branch + ".yaml")
                self.cmd.replacement(self.path.helm_chart_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                self.cmd.replacement(self.path.helm_values_dev_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_PROJECT_NAME__', self.gitlab_env.CI_PROJECT_NAME + "/" + MODULE)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_APPLICATION_NAME__', MODULE)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_HELM_NAMESPACE__', self.gitlab_env.CD_HELM_NAMESPACE)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_GROUP_NAME__', self.gitlab_env.CI_GROUP_NAME)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_SUBGROUP_NAME__', self.gitlab_env.CI_SUBGROUP_NAME)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_HELM_CONTAINER_PORT__', self.gitlab_env.CD_HELM_CONTAINER_PORT)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_HELM_MANAGEMENT_PORT__', self.gitlab_env.CD_HELM_MANAGEMENT_PORT)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_HELM_SERVICE_PORT__', self.gitlab_env.CD_HELM_SERVICE_PORT)
                self.cmd.replacement(self.path.helm_values_dev_yaml, '__CD_HELM_DOMAIN_NAME__', self.gitlab_env.CD_HELM_DOMAIN_NAME_DEV)
            elif branch == "master":
                self.cmd.recursive_copy(self.path.helm_chart_source_path, self.path.helm_chart_destination_path)
                rename(self.path.helm_chart_destination_path + 'values.yaml', self.path.helm_chart_destination_path + branch + ".yaml")
                remove(self.path.helm_values_dev_yaml)
                self.cmd.replacement(self.path.helm_chart_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                self.cmd.replacement(self.path.helm_values_master_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_PROJECT_NAME__', self.gitlab_env.CI_PROJECT_NAME + "/" + MODULE)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_APPLICATION_NAME__', MODULE)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_HELM_NAMESPACE__', self.gitlab_env.CD_HELM_NAMESPACE)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_GROUP_NAME__', self.gitlab_env.CI_GROUP_NAME)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_SUBGROUP_NAME__', self.gitlab_env.CI_SUBGROUP_NAME)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_HELM_CONTAINER_PORT__', self.gitlab_env.CD_HELM_CONTAINER_PORT)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_HELM_MANAGEMENT_PORT__', self.gitlab_env.CD_HELM_MANAGEMENT_PORT)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_HELM_SERVICE_PORT__', self.gitlab_env.CD_HELM_SERVICE_PORT)
                self.cmd.replacement(self.path.helm_values_master_yaml, '__CD_HELM_DOMAIN_NAME__', self.gitlab_env.CD_HELM_DOMAIN_NAME_PROD)
            
            system('git add .')
            system("git status")
            system("git commit -am 'Configured project'")
            system("git push --set-upstream origin " + branch)
        
        path_parent = path.dirname(getcwd())
        chdir(path_parent)

    def push_to_application(self):
        MODULE = ""
        if self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE != "NULL":
            MODULE = self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE
        else:
            MODULE = self.gitlab_env.CI_PROJECT_NAME
        chdir(self.path.argo_application_path)
        self.cmd.create_folder(self.gitlab_env.CI_PROJECT_NAME)
        argo_application_yaml = self.path.argo_application_destination_path + self.gitlab_env.CI_PROJECT_NAME + "/" + self.gitlab_env.CI_PROJECT_NAME + "-application.yaml"
        argo_gitlab_ci_yaml = self.path.argo_application_destination_path + ".gitlab-ci.yml"
        
        for branch in self.gitlab_env.branches:
            system('git checkout -b' + branch)
            if branch == "develop":
                self.cmd.file_copy(self.path.argo_template_source_path + "application.yaml", argo_application_yaml)
                self.cmd.replacement(argo_application_yaml, '__CD_PROJECT_NAME__', MODULE)
                self.cmd.replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', MODULE)
                self.cmd.replacement(argo_application_yaml, '__CD_SUBGROUP_NAME__', self.gitlab_env.CI_SUBGROUP_NAME)
                self.cmd.replacement(argo_application_yaml, '__CD_HELM_NAMESPACE__', self.gitlab_env.CD_HELM_NAMESPACE)
                self.cmd.replacement(argo_application_yaml, '__CD_GROUP_NAME__', self.gitlab_env.CD_GROUP_NAME)
                self.cmd.replacement(argo_application_yaml, '__CI_BRANCH_NAME__', branch)
                self.cmd.replacement(argo_application_yaml, '__CI_ENVIRONMENT_NAME__', "dev")
                self.cmd.file_copy(self.path.argo_gitlab_ci_application_template, argo_gitlab_ci_yaml)
                self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', self.gitlab_env.CI_PROJECT_TYPE_FRONTEND)
                self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND)
                self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND_DMZ__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ)
            if branch == "master":
                self.cmd.file_copy(self.path.argo_template_source_path + "application.yaml", argo_application_yaml)
                self.cmd.replacement(argo_application_yaml, '__CD_PROJECT_NAME__', MODULE)
                self.cmd.replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', MODULE)
                self.cmd.replacement(argo_application_yaml, '__CD_SUBGROUP_NAME__', self.gitlab_env.CI_SUBGROUP_NAME)
                self.cmd.replacement(argo_application_yaml, '__CD_PROJECT_NAME__', self.gitlab_env.CI_PROJECT_NAME)
                self.cmd.replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', self.gitlab_env.CI_PROJECT_NAME)
                self.cmd.replacement(argo_application_yaml, '__CD_HELM_NAMESPACE__', self.gitlab_env.CD_HELM_NAMESPACE)
                self.cmd.replacement(argo_application_yaml, '__CD_GROUP_NAME__', self.gitlab_env.CD_GROUP_NAME)
                self.cmd.replacement(argo_application_yaml, '__CI_BRANCH_NAME__', branch)
                self.cmd.replacement(argo_application_yaml, '__CI_ENVIRONMENT_NAME__', "prod")
                self.cmd.file_copy(self.path.argo_gitlab_ci_application_template, argo_gitlab_ci_yaml)
                self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', self.gitlab_env.CI_PROJECT_TYPE_FRONTEND)
                self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND)
                self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND_DMZ__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ)
            
            system('git add .')
            system("git status")
            system("git commit -am 'Updated application.yaml'")
            system("git push --set-upstream origin " + branch)
        
        path_parent = path.dirname(getcwd())
        chdir(path_parent)

    def push_to_project(self):        
        chdir(self.path.argo_project_path)
        self.cmd.create_folder(self.gitlab_env.CI_SUBGROUP_NAME)
        argo_project_yaml = self.path.argo_project_destination_path + self.gitlab_env.CI_SUBGROUP_NAME + "/" +self.gitlab_env. CI_SUBGROUP_NAME + "-project.yaml"
        argo_gitlab_ci_yaml = self.path.argo_project_destination_path + ".gitlab-ci.yml"
        for branch in self.gitlab_env.branches:
            system('git checkout -b' + branch)
            self.cmd.file_copy(self.path.argo_template_source_path + "project.yaml", argo_project_yaml)
            self.cmd.replacement(argo_project_yaml, '__CD_SUBGROUP_NAME__', self.gitlab_env.CI_SUBGROUP_NAME)
            self.cmd.replacement(argo_project_yaml, '__CD_HELM_NAMESPACE__', self.gitlab_env.CD_HELM_NAMESPACE)
            self.cmd.file_copy(self.path.argo_gitlab_ci_project_template, argo_gitlab_ci_yaml)
            self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', self.gitlab_env.CI_PROJECT_TYPE_FRONTEND)
            self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND)
            self.cmd.replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND_DMZ__', self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ)
            
            system('git add .')
            system("git status")
            system("git commit -am 'Updated project.yaml'")
            system("git push --set-upstream origin " + branch)
        
        path_parent = path.dirname(getcwd())
        chdir(path_parent)