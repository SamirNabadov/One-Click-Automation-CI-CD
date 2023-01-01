from os import getenv, getcwd

class GitlabAuthConf():
    CI_GITLAB_SERVER        = getenv("CI_SERVER_URL")
    CI_GITLAB_TOKEN_NAME    = getenv("CI_GITLAB_TOKEN_NAME")
    CI_GITLAB_TOKEN         = getenv("CI_GITLAB_TOKEN")
    CI_GITLAB_SSL_VERIFY    = False
    CI_GITLAB_API_VERSION   = "4"

class GitlabEnvConf():
    CI_SUBGROUP_NAME                        = getenv("CI_SUBGROUP_NAME")
    CI_PROJECT_NAME                         = getenv("CI_PROJECT_NAME")
    CI_PROJECT_GENERATION                   = getenv("CI_PROJECT_GENERATION")
    CI_PROJECT_MIGRATION                    = getenv("CI_PROJECT_MIGRATION")
    CI_PROJECT_TYPE_FRONTEND                = getenv("CI_PROJECT_TYPE_FRONTEND")
    CI_PROJECT_TYPE_BACKEND                 = getenv("CI_PROJECT_TYPE_BACKEND")
    CI_PROJECT_TYPE_BACKEND_DMZ             = getenv("CI_PROJECT_TYPE_BACKEND_DMZ")
    CI_PROJECT_MODE_MONO_REPO               = getenv("CI_PROJECT_MODE_MONO_REPO")
    CI_PROJECT_MODE_MULTI_MODULE            = getenv("CI_PROJECT_MODE_MULTI_MODULE")
    CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE = getenv("CI_MODULE_NAME_FOR_MULTI_MDOULE")
    CI_APPLICATION_TYPE_MAVEN               = getenv("CI_APPLICATION_TYPE_MAVEN")
    CI_APPLICATION_TYPE_GRADLE              = getenv("CI_APPLICATION_TYPE_GRADLE")
    CI_APPLICATION_TYPE_PYTHON              = getenv("CI_APPLICATION_TYPE_PYTHON")
    CI_RELEASE_TYPE_JIB                     = getenv("CI_RELEASE_TYPE_JIB")
    CI_RELEASE_TYPE_KANIKO                  = getenv("CI_RELEASE_TYPE_KANIKO")
    CI_CODE_STYLE_SONARQUBE                 = getenv("CI_CODE_STYLE_SONARQUBE")
    CI_CODE_CHECK_SNYK                      = getenv("CI_CODE_CHECK_SNYK")
    CI_PROJECT_TEST_STAGE                   = getenv("CI_PROJECT_TEST_STAGE")
    CI_BACKEND_IMAGE_VERSION_GRADLE         = getenv("CI_BACKEND_IMAGE_VERSION_GRADLE")
    CI_BACKEND_IMAGE_VERSION_MAWEN          = getenv("CI_BACKEND_IMAGE_VERSION_MAWEN")
    CD_HELM_NAMESPACE                       = getenv("CD_HELM_NAMESPACE")
    CD_HELM_CONTAINER_PORT                  = getenv("CD_HELM_CONTAINER_PORT")
    CD_HELM_MANAGEMENT_PORT                 = getenv("CD_HELM_MANAGEMENT_PORT")
    CD_HELM_SERVICE_PORT                    = getenv("CD_HELM_SERVICE_PORT")
    CD_HELM_DOMAIN_NAME_DEV                 = getenv("CD_HELM_DOMAIN_NAME_DEV")
    CD_HELM_DOMAIN_NAME_PROD                = getenv("CD_HELM_DOMAIN_NAME_PROD")
    CI_ACCESS_MAINTAINER                    = getenv("CI_ACCESS_MAINTAINER")
    CI_ACCESS_DEVELOPER                     = getenv("CI_ACCESS_DEVELOPER")
    CI_ACCESS_REPORTER                      = "".join([CI_ACCESS_MAINTAINER," ", CI_ACCESS_DEVELOPER])
    CI_MAIN_GROUP                           = "development"
    CD_GROUP_NAME                           = "".join([CI_MAIN_GROUP,'/chart'])
    CI_GROUP_NAME                           = "".join([CI_MAIN_GROUP,'/code'])
    CI_TEMPLATE_PROJECT_NAME                = "devops/cicd-template"
    CI_GITLAB_HOSTNAME                      = "gitlab.local.lan"
    code_subgroup_id, chart_subgroup_id     = 453, 452
    application_subgroup_id                 = 451
    project_subgroup_id                     = 450
    CI_IMAGE_REPO_ID, CI_TEMPLATE_REPO_ID   = 230, 827
    visibility                              = 'private'
    branches                                = ["develop", 'master']

class ContainerExprPolicy:
    ENABLED             = True
    TIME_CLEANUP        = "7d"
    TAGS_COUNT_KEEP     = 5
    NAME_REGEX_KEEP     = 'dev-*, prod-*'
    TIME_TAGS_DELETE    = "30d"
    NAME_REGEX_DELETE   = 'dev-*, prod-*'

class ArgoEnvConf():
    CI_ARGO_GITLAB_USERNAME  = getenv("CI_ARGO_GITLAB_USERNAME")
    CI_ARGO_GITLAB_PASSWORD  = getenv("CI_ARGO_GITLAB_PASSWORD")
    CI_ARGO_SERVER_DEV       = getenv("CI_ARGO_SERVER_DEV")
    CI_ARGO_USERNAME_DEV     = getenv("CI_ARGO_USERNAME_DEV")
    CI_ARGO_PASSWORD_DEV     = getenv("CI_ARGO_PASSWORD_DEV")
    CI_ARGO_SERVER_DEVDMZ    = getenv("CI_ARGO_SERVER_DEVDMZ")
    CI_ARGO_USERNAME_DEVDMZ  = getenv("CI_ARGO_USERNAME_DEVDMZ")
    CI_ARGO_PASSWORD_DEVDMZ  = getenv("CI_ARGO_PASSWORD_DEVDMZ")
    CI_ARGO_SERVER_PROD      = getenv("CI_ARGO_SERVER_PROD")
    CI_ARGO_USERNAME_PROD    = getenv("CI_ARGO_USERNAME_PROD")
    CI_ARGO_PASSWORD_PROD    = getenv("CI_ARGO_PASSWORD_PROD")
    CI_ARGO_SERVER_PRODDMZ   = getenv("CI_ARGO_SERVER_PRODDMZ")
    CI_ARGO_USERNAME_PRODDMZ = getenv("CI_ARGO_USERNAME_PRODDMZ")
    CI_ARGO_PASSWORD_PRODDMZ = getenv("CI_ARGO_PASSWORD_PRODDMZ")

class PathConf():
    current_directory                               = getcwd()
    helm_chart_path, gitlab_ci_path                 = 'helm-charts', 'ci-template'
    argo_template_path                              = "argo-template"
    argo_application_path, argo_project_path        = "application", "project"
    gradle_single_module_path                       = 'gradle-single-module-template'
    gradle_multi_module_path                        = 'gradle-multi-module-template'
    code_path, chart_path                           = 'code', 'chart'
    application_path, project_path                  = 'application', 'project'
    gradle_settings                                 = "".join([current_directory,'/',code_path,'/',"settings.gradle"])
    gradle_application_yaml                         = "".join([current_directory,'/',code_path,"/src/main/resources/application.yaml"])
    gitlab_ci_source_path                           = "".join([current_directory,'/',gitlab_ci_path,'/gitlab-ci-for-projects.yml'])
    gitlab_ci_destination_path = gitlab_ci_yaml     = "".join([current_directory,'/',code_path,'/.gitlab-ci.yml'])
    project_gradle_single_module_source_path        = "".join([current_directory,'/',gradle_single_module_path,'/'])
    project_gradle_multi_module_source_path         = "".join([current_directory,'/',gradle_multi_module_path,'/'])
    project_destination_folder                      = "".join([current_directory,'/',code_path,'/'])
    helm_chart_source_path                          = "".join([current_directory,'/',helm_chart_path,'/'])
    helm_chart_destination_path                     = "".join([current_directory,'/',chart_path,'/'])
    helm_chart_yaml                                 = "".join([current_directory,'/',chart_path,'/Chart.yaml'])
    helm_values_dev_yaml                            = "".join([current_directory,'/',chart_path,'/develop.yaml'])
    helm_values_master_yaml                         = "".join([current_directory,'/',chart_path,'/master.yaml'])
    argo_template_source_path                       = "".join([current_directory,'/',argo_template_path,'/'])
    argo_application_destination_path               = "".join([current_directory,'/',argo_application_path,'/'])
    argo_project_destination_path                   = "".join([current_directory,'/',argo_project_path,'/'])
    argo_gitlab_ci_application_template             = "".join([current_directory,'/',gitlab_ci_path,'/gitlab-ci-argo-application.yml'])
    argo_gitlab_ci_project_template                 = "".join([current_directory,'/',gitlab_ci_path,'/gitlab-ci-argo-project.yml'])


