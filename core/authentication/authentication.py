from core.configuration.variables import GitlabEnvConf, PathConf, ArgoEnvConf
from urllib3 import disable_warnings, exceptions
import gitlab, logging
from os import system

"""
Disabling Gitlab warnings due to self-signed certificate usage
"""
disable_warnings(exceptions.InsecureRequestWarning)

class GitlabAuth():
    def connect(self, ssl_verify, gitlab_server, token, api_version):
        self.ssl_verify = ssl_verify
        self.gitlab_server = gitlab_server
        self.token = token
        self.api_version = api_version

        gitlab_session = gitlab.Gitlab(url=self.gitlab_server,
                                       private_token=self.token,
                                       ssl_verify=self.ssl_verify,
                                       api_version=self.api_version)
        gitlab_session.auth()
        try:
            gitlab_session.version()
        except (gitlab.exceptions.GitlabAuthenticationError):
            raise RuntimeError("Invalid or missing GITLAB TOKEN")

        logging.info("Connected to: %s", self.gitlab_server)
        return gitlab_session

class ArgoAuth():
    path             = PathConf()
    gitlab_env       = GitlabEnvConf()
    argo_env         = ArgoEnvConf()

    def connect(self, argo_server, argo_username, argo_password):
        self.argo_server = argo_server
        self.argo_username = argo_username
        self.argo_password = argo_password

        system("".join(['argocd login ', self.argo_server, ' --insecure --username ', self.argo_username, ' --password ', self.argo_password]))

    def add_repository(self, project_name):
        self.project_name = project_name

        system(f"argocd repo add https://{self.gitlab_env.CI_GITLAB_HOSTNAME}/{self.gitlab_env.CI_MAIN_GROUP}/{self.path.chart_path}/{self.gitlab_env.CI_SUBGROUP_NAME}/{self.project_name}.git --username {self.argo_env.CI_ARGO_GITLAB_USERNAME} --password {self.argo_env.CI_ARGO_GITLAB_PASSWORD} --insecure-skip-server-verification")
