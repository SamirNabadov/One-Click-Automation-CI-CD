from os import system
from core.operation.command import Command
from core.configuration.variables import PathConf, GitlabEnvConf, GitlabAuthConf
from git import Repo

class GitCloneOps():
    cmd              = Command()
    path             = PathConf()
    gitlab_env       = GitlabEnvConf()
    gitlab_auth_conf = GitlabAuthConf()

    def template_helm_chart(self):
        self.cmd.create_folder(self.path.helm_chart_path)
        self.cmd.delete_folder(self.path.helm_chart_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_TEMPLATE_PROJECT_NAME,"/",self.path.helm_chart_path,".git"])
        path = self.path.helm_chart_path
        Repo.clone_from(url, path)
        self.cmd.delete_folder("".join([self.path.helm_chart_source_path,".git"]))

    def template_gitlab_ci(self):
        self.cmd.create_folder(self.path.gitlab_ci_path)
        self.cmd.delete_folder(self.path.gitlab_ci_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_TEMPLATE_PROJECT_NAME,"/",self.path.gitlab_ci_path,".git"])
        path = self.path.gitlab_ci_path
        Repo.clone_from(url, path)
        self.cmd.delete_folder("".join([self.path.gitlab_ci_source_path,".git"]))

    def tempalte_gradle_single_module(self):
        self.cmd.create_folder(self.path.gradle_single_module_path)
        self.cmd.delete_folder(self.path.gradle_single_module_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_TEMPLATE_PROJECT_NAME,"/",self.path.gradle_single_module_path,".git"])
        path = self.path.gradle_single_module_path
        Repo.clone_from(url, path)
        self.cmd.delete_folder("".join([self.path.project_gradle_single_module_source_path,".git"]))

    def tempalte_gradle_multi_module(self):
        self.cmd.create_folder(self.path.gradle_multi_module_path)
        self.cmd.delete_folder(self.path.gradle_multi_module_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_TEMPLATE_PROJECT_NAME,"/",self.path.gradle_multi_module_path,".git"])
        path = self.path.gradle_multi_module_path
        Repo.clone_from(url, path)
        self.cmd.delete_folder(self.path.project_gradle_multi_module_source_path + ".git")

    def template_argocd(self):
        self.cmd.create_folder(self.path.argo_template_path)
        self.cmd.delete_folder(self.path.argo_template_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_TEMPLATE_PROJECT_NAME,"/",self.path.argo_template_path,".git"])
        path = self.path.argo_template_path
        Repo.clone_from(url, path)
        self.cmd.delete_folder("".join([self.path.argo_template_source_path,".git"]))

    def repo_source_code(self):
        self.cmd.create_folder(self.path.code_path)
        self.cmd.delete_folder(self.path.code_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_MAIN_GROUP,"/",self.path.code_path,"/",self.gitlab_env.CI_SUBGROUP_NAME,"/",self.gitlab_env.CI_PROJECT_NAME,".git"])
        path = self.path.code_path
        Repo.clone_from(url, path)

    def repo_helm_chart(self, project_name):
        self.project_name = project_name

        self.cmd.create_folder(self.path.chart_path)
        self.cmd.delete_folder(self.path.chart_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_MAIN_GROUP,"/",self.path.chart_path,"/",self.gitlab_env.CI_SUBGROUP_NAME,"/",self.project_name,".git"])
        path = self.path.chart_path
        Repo.clone_from(url, path)

    def repo_argo_application(self, project_name):
        self.project_name = project_name
        
        self.cmd.create_folder(self.path.application_path)
        self.cmd.delete_folder(self.path.application_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_MAIN_GROUP,"/",self.path.application_path,"/",self.gitlab_env.CI_SUBGROUP_NAME,"/",self.project_name,".git"])
        path = self.path.application_path
        Repo.clone_from(url, path)

    def repo_argo_project(self):
        self.cmd.create_folder(self.path.project_path)
        self.cmd.delete_folder(self.path.project_path)
        url = "".join(["https://",self.gitlab_auth_conf.CI_GITLAB_TOKEN_NAME,":",self.gitlab_auth_conf.CI_GITLAB_TOKEN,"@",self.gitlab_env.CI_GITLAB_HOSTNAME,"/",self.gitlab_env.CI_MAIN_GROUP,"/",self.path.project_path,"/",self.gitlab_env.CI_SUBGROUP_NAME,".git"])
        path = self.path.project_path
        Repo.clone_from(url, path)