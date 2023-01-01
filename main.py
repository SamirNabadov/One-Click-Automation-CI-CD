from core.configuration.variables import GitlabEnvConf, ArgoEnvConf
from core.configuration.validation import Validation
from core.authentication.authentication import ArgoAuth
from core.operation.command import Command
from core.operation.project import GitlabProjOps
from core.operation.clone import GitCloneOps
from core.operation.push import GitPushOps
from os import environ, system

class Application():
    """
    Disable ssl verify for git repositories
    """
    environ["GIT_SSL_NO_VERIFY"] = 'True'

    validation       = Validation()
    operation        = GitlabProjOps()
    clone            = GitCloneOps()
    push             = GitPushOps()
    gitlab_env       = GitlabEnvConf()
    argo             = ArgoAuth()
    argo_env         = ArgoEnvConf()
    cmd              = Command()

    MODULE = ""

    def run(self):  
        self.cmd.clear()
        if self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE != "NULL":
            self.MODULE = self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE
        else:
            self.MODULE = self.gitlab_env.CI_PROJECT_NAME

        self.operation.create_groups()
        self.operation.create_projects()
        self.clone.template_helm_chart()
        self.clone.template_gitlab_ci()
        if self.gitlab_env.CI_PROJECT_GENERATION == "TRUE" and self.gitlab_env.CI_PROJECT_MODE_MONO_REPO == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE":
            self.clone.tempalte_gradle_single_module()
        elif self.gitlab_env.CI_PROJECT_GENERATION == "TRUE" and self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE":
            self.clone.tempalte_gradle_multi_module()

        self.clone.template_argocd()
        self.clone.repo_source_code()
        self.clone.repo_helm_chart(self.MODULE)
        self.clone.repo_argo_application(self.MODULE)
        self.clone.repo_argo_project()
        self.push.push_to_code()
        self.push.push_to_chart()
        if self.gitlab_env.CI_PROJECT_TYPE_BACKEND == "TRUE" and self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ == "FALSE":
            self.argo.connect(self.argo_env.CI_ARGO_SERVER_DEV, 
                              self.argo_env.CI_ARGO_USERNAME_DEV, 
                              self.argo_env.CI_ARGO_PASSWORD_DEV)
            self.argo.add_repository(self.MODULE)
            self.argo.connect(self.argo_env.CI_ARGO_SERVER_PROD, 
                              self.argo_env.CI_ARGO_USERNAME_PROD, 
                              self.argo_env.CI_ARGO_PASSWORD_PROD)
            self.argo.add_repository(self.MODULE)
        elif (self.gitlab_env.CI_PROJECT_TYPE_BACKEND == "TRUE" and self.gitlab_env.CI_PROJECT_TYPE_BACKEND_DMZ == "TRUE") or self.gitlab_env.CI_PROJECT_TYPE_FRONTEND == "TRUE":
            self.argo.connect(self.argo_env.CI_ARGO_SERVER_DEVDMZ, 
                              self.argo_env.CI_ARGO_USERNAME_DEVDMZ, 
                              self.argo_env.CI_ARGO_PASSWORD_DEVDMZ)
            self.argo.add_repository(self.MODULE)
            self.argo.connect(self.argo_env.CI_ARGO_SERVER_PRODDMZ, 
                              self.argo_env.CI_ARGO_USERNAME_PRODDMZ, 
                              self.argo_env.CI_ARGO_PASSWORD_PRODDMZ)
            self.argo.add_repository(self.MODULE)

        self.push.push_to_project()
        self.push.push_to_application()


if __name__ == '__main__':
    app = Application()
    app.run()