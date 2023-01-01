from core.configuration.variables import GitlabEnvConf

"""
Defined variables from CI/CD Pipeline.
Function for validation of variables
"""
class Validation():
    env = GitlabEnvConf()

    def check_environment_variables(self):
        if self.gitlab_env.CI_PROJECT_GENERATION == self.gitlab_env.CI_PROJECT_MIGRATION:
            exit("CI_PROJECT_GENERATION and CI_PROJECT_MIGRATION must not be same. Process killed!")
        elif self.gitlab_env.CI_PROJECT_TYPE_FRONTEND ==self.gitlab_env.CI_PROJECT_TYPE_BACKEND:
            exit("CI_PROJECT_TYPE_FRONTEND and CI_PROJECT_TYPE_BACKEND must not be same. Process killed!")
        elif self.gitlab_env.CI_PROJECT_MODE_MONO_REPO == self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE:
            exit("CI_PROJECT_MODE_MONO_REPO and CI_PROJECT_MODE_MULTI_MODULE must not be same. Process killed!")
        elif (self.gitlab_env.CI_APPLICATION_TYPE_MAVEN == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE") or (self.gitlab_env.CI_APPLICATION_TYPE_MAVEN == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_PYTHON == "TRUE") or (self.gitlab_env.CI_APPLICATION_TYPE_GRADLE == "TRUE" and self.gitlab_env.CI_APPLICATION_TYPE_PYTHON == "TRUE"):
            exit("CI_APPLICATION_TYPE_MAVEN or CI_APPLICATION_TYPE_GRADLE or CI_APPLICATION_TYPE_PYTHON must not be 'TRUE' in same time. Process killed!")
        elif self.gitlab_env.CI_RELEASE_TYPE_JIB == self.gitlab_env.CI_RELEASE_TYPE_KANIKO:
            exit("CI_RELEASE_TYPE_JIB and CI_RELEASE_TYPE_KANIKO must not be same. Process killed!")
        else:
            print("The operation was successfully validated!")