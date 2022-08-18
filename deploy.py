#!/usr/bin/env python3

from modules.functions import *
import os, sys, subprocess
import urllib3

os.environ["GIT_SSL_NO_VERIFY"] = 'True'
visibility = 'private'
ssl_verify = False

CI_GITLAB_SERVER = os.getenv("CI_SERVER_URL")
CI_GITLAB_TOKEN_NAME = os.getenv("CI_GITLAB_TOKEN_NAME")
CI_GITLAB_TOKEN = os.getenv("CI_GITLAB_TOKEN")

CI_ARGO_GITLAB_USERNAME = os.getenv("CI_ARGO_GITLAB_USERNAME")
CI_ARGO_GITLAB_PASSWORD = os.getenv("CI_ARGO_GITLAB_PASSWORD")

CI_ARGO_USERNAME_DEV = os.getenv("CI_ARGO_USERNAME_DEV")
CI_ARGO_PASSWORD_DEV = os.getenv("CI_ARGO_PASSWORD_DEV")
CI_ARGO_SERVER_DEV = os.getenv("CI_ARGO_SERVER_DEV")
CI_ARGO_USERNAME_DEVDMZ = os.getenv("CI_ARGO_USERNAME_DEVDMZ")
CI_ARGO_PASSWORD_DEVDMZ = os.getenv("CI_ARGO_PASSWORD_DEVDMZ")
CI_ARGO_SERVER_DEVDMZ = os.getenv("CI_ARGO_SERVER_DEVDMZ")
CI_ARGO_USERNAME_PROD = os.getenv("CI_ARGO_USERNAME_PROD")
CI_ARGO_PASSWORD_PROD = os.getenv("CI_ARGO_PASSWORD_PROD")
CI_ARGO_SERVER_PROD = os.getenv("CI_ARGO_SERVER_PROD")
CI_ARGO_USERNAME_PRODDMZ = os.getenv("CI_ARGO_USERNAME_PRODDMZ")
CI_ARGO_PASSWORD_PRODDMZ = os.getenv("CI_ARGO_PASSWORD_PRODDMZ")
CI_ARGO_SERVER_PRODDMZ = os.getenv("CI_ARGO_SERVER_PRODDMZ")

CI_SUBGROUP_NAME = os.getenv("CI_SUBGROUP_NAME")
CI_PROJECT_NAME = os.getenv("CI_PROJECT_NAME")
CI_PROJECT_GENERATION = os.getenv("CI_PROJECT_GENERATION")
CI_PROJECT_MIGRATION = os.getenv("CI_PROJECT_MIGRATION")
CI_PROJECT_TYPE_FRONTEND = os.getenv("CI_PROJECT_TYPE_FRONTEND")
CI_PROJECT_TYPE_BACKEND = os.getenv("CI_PROJECT_TYPE_BACKEND")
CI_PROJECT_MODE_MONO_REPO = os.getenv("CI_PROJECT_MODE_MONO_REPO")
CI_PROJECT_MODE_MULTI_MODULE = os.getenv("CI_PROJECT_MODE_MULTI_MODULE")
CI_PROJECT_MULTI_MODULE_NAMES = os.getenv("CI_PROJECT_MULTI_MODULE_NAMES")
CI_APPLICATION_TYPE_MAVEN = os.getenv("CI_APPLICATION_TYPE_MAVEN")
CI_APPLICATION_TYPE_GRADLE = os.getenv("CI_APPLICATION_TYPE_GRADLE")
CI_RELEASE_TYPE_JIB = os.getenv("CI_RELEASE_TYPE_JIB")
CI_RELEASE_TYPE_KANIKO = os.getenv("CI_RELEASE_TYPE_KANIKO")
CI_CODE_STYLE_SONARQUBE = os.getenv("CI_CODE_STYLE_SONARQUBE")
CI_CODE_CHECK_SNYK = os.getenv("CI_CODE_CHECK_SNYK")
CI_PROJECT_TEST_STAGE = os.getenv("CI_PROJECT_TEST_STAGE")

CD_HELM_NAMESPACE = os.getenv("CD_HELM_NAMESPACE")
CD_HELM_CONTAINER_PORT = os.getenv("CD_HELM_CONTAINER_PORT")
CD_HELM_MANAGEMENT_PORT = os.getenv("CD_HELM_MANAGEMENT_PORT")
CD_HELM_SERVICE_PORT = os.getenv("CD_HELM_SERVICE_PORT")
CD_HELM_DOMAIN_NAME_DEV = os.getenv("CD_HELM_DOMAIN_NAME_DEV")
CD_HELM_DOMAIN_NAME_PROD = os.getenv("CD_HELM_DOMAIN_NAME_PROD")

CI_GROUP_NAME = 'development/code'
CD_GROUP_NAME = 'development/chart'

# Set branch names in the list
# Branches in the functions are considered only according to 2 branches (develop/master)
branches = ["develop", 'master']

# Set id of the subgroups under the main group 
code_subgroup_id = 453
chart_subgroup_id = 452
application_subgroup_id = 451
project_subgroup_id = 450

current_directory = os.getcwd()
MODULES = []
PROJECT_EXISTS = False

helm_chart_path = 'helm-charts'
gitlab_ci_path = 'ci-template'
gradle_single_module_path = 'gradle-single-module-template'
gradle_multi_module_path = 'gradle-multi-module-template'

code_path = 'code'
chart_path = 'chart'
application_path = 'application'
project_path = 'project'

wordCheck = "include"
moduleCheck = "common"

gradle_settings = current_directory + "/" + code_path + "/" + "settings.gradle"
gradle_application_yaml = current_directory + "/" + code_path + "/src/main/resources/application.yaml"

gitlab_ci_source_path = current_directory + '/' + gitlab_ci_path + '/gitlab-ci-for-projects.yml'
gitlab_ci_destination_path = gitlab_ci_yaml = current_directory + '/' + code_path + '/.gitlab-ci.yml'

project_gradle_single_module_source_path = current_directory + '/' + gradle_single_module_path + '/'
project_gradle_multi_module_source_path = current_directory + '/' + gradle_multi_module_path + '/'
project_destination_folder = current_directory + '/' + code_path + '/'

helm_chart_source_path = current_directory + '/' + helm_chart_path + '/'
helm_chart_destination_path = current_directory + "/" + chart_path +  "/"

helm_chart_yaml = current_directory + '/' + chart_path + '/Chart.yaml'
helm_values_dev_yaml = current_directory + '/' + chart_path + '/develop.yaml' 
helm_values_master_yaml = current_directory + '/' + chart_path + '/master.yaml'

argo_template_path = "argo-template"
argo_application_path = "application"
argo_project_path = "project"

argo_template_source_path = current_directory + '/' + argo_template_path + '/'
argo_application_destination_path = current_directory + "/" + argo_application_path +  "/"
argo_project_destination_path = current_directory + "/" + argo_project_path +  "/"

argo_gitlab_ci_application_template = current_directory + '/' + gitlab_ci_path + '/gitlab-ci-argo-application.yml'
argo_gitlab_ci_project_template = current_directory + '/' + gitlab_ci_path + '/gitlab-ci-argo-project.yml'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def git_push_to_code(repo_path, branches, gitlab_ci_yaml):
    os.chdir(repo_path)
    for branch in branches:
        os.system('git checkout -b' + branch)
        if branch == "develop":
            file_copy(gitlab_ci_source_path, gitlab_ci_destination_path)
            if CI_PROJECT_GENERATION == "TRUE" and CI_PROJECT_TYPE_BACKEND == "TRUE" and CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
                recursive_copy(project_gradle_multi_module_source_path, project_destination_folder)
                replacement(gradle_settings,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            elif CI_PROJECT_GENERATION == "TRUE" and CI_PROJECT_TYPE_BACKEND == "TRUE" and CI_PROJECT_MODE_MONO_REPO == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
                recursive_copy(project_gradle_single_module_source_path, project_destination_folder)
                replacement(gradle_settings,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
                replacement(gradle_application_yaml,'__CD_HELM_CONTAINER_PORT__', CD_HELM_CONTAINER_PORT)
                replacement(gradle_application_yaml,'__CD_HELM_MANAGEMENT_PORT__', CD_HELM_MANAGEMENT_PORT)

            replacement(gitlab_ci_yaml,'__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_MODE_MONO_REPO__', CI_PROJECT_MODE_MONO_REPO)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_MODE_MULTI_MODULE__', CI_PROJECT_MODE_MULTI_MODULE)
            replacement(gitlab_ci_yaml,'__CI_APPLICATION_TYPE_MAVEN__', CI_APPLICATION_TYPE_MAVEN)
            replacement(gitlab_ci_yaml,'__CI_APPLICATION_TYPE_GRADLE__',CI_APPLICATION_TYPE_GRADLE )
            replacement(gitlab_ci_yaml,'__CI_RELEASE_TYPE_JIB__', CI_RELEASE_TYPE_JIB)
            replacement(gitlab_ci_yaml,'__CI_RELEASE_TYPE_KANIKO__', CI_RELEASE_TYPE_KANIKO)
            replacement(gitlab_ci_yaml,'__CI_CODE_STYLE_SONARQUBE__', CI_CODE_STYLE_SONARQUBE)
            replacement(gitlab_ci_yaml,'__CI_CODE_CHECK_SNYK__', CI_CODE_CHECK_SNYK)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_TEST_STAGE__', CI_PROJECT_TEST_STAGE)
        elif branch == "master":
            file_copy(gitlab_ci_source_path, gitlab_ci_destination_path)
            if CI_PROJECT_GENERATION == "TRUE" and CI_PROJECT_TYPE_BACKEND == "TRUE" and CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
                recursive_copy(project_gradle_multi_module_source_path, project_destination_folder)
                replacement(gradle_settings,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            elif CI_PROJECT_GENERATION == "TRUE" and CI_PROJECT_TYPE_BACKEND == "TRUE" and CI_PROJECT_MODE_MONO_REPO == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
                recursive_copy(project_gradle_single_module_source_path, project_destination_folder)
                replacement(gradle_settings,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
                replacement(gradle_application_yaml,'__CD_HELM_CONTAINER_PORT__', CD_HELM_CONTAINER_PORT)
                replacement(gradle_application_yaml,'__CD_HELM_MANAGEMENT_PORT__', CD_HELM_MANAGEMENT_PORT)

            replacement(gitlab_ci_yaml,'__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_MODE_MONO_REPO__', CI_PROJECT_MODE_MONO_REPO)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_MODE_MULTI_MODULE__', CI_PROJECT_MODE_MULTI_MODULE)
            replacement(gitlab_ci_yaml,'__CI_APPLICATION_TYPE_MAVEN__', CI_APPLICATION_TYPE_MAVEN)
            replacement(gitlab_ci_yaml,'__CI_APPLICATION_TYPE_GRADLE__', CI_APPLICATION_TYPE_GRADLE)
            replacement(gitlab_ci_yaml,'__CI_RELEASE_TYPE_JIB__', CI_RELEASE_TYPE_JIB)
            replacement(gitlab_ci_yaml,'__CI_RELEASE_TYPE_KANIKO__', CI_RELEASE_TYPE_KANIKO)
            replacement(gitlab_ci_yaml,'__CI_CODE_STYLE_SONARQUBE__', CI_CODE_STYLE_SONARQUBE)
            replacement(gitlab_ci_yaml,'__CI_CODE_CHECK_SNYK__', CI_CODE_CHECK_SNYK)
            replacement(gitlab_ci_yaml,'__CI_PROJECT_TEST_STAGE__', CI_PROJECT_TEST_STAGE)

        os.system('git add .')
        os.system("git status")
        os.system("git commit -am 'Configured project'")
        os.system("git push --set-upstream origin " + branch)

    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def git_push_to_chart(repo_path, branches, helm_chart_yaml, helm_values_dev_yaml, helm_values_master_yaml):
    os.chdir(repo_path)
    for branch in branches:
        os.system('git checkout -b' + branch)
        if branch == "develop":
            recursive_copy(helm_chart_source_path, helm_chart_destination_path)
            os.rename(helm_chart_destination_path + 'values.yaml', helm_chart_destination_path + branch + ".yaml")
            replacement(helm_chart_yaml,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_dev_yaml,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_dev_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
            replacement(helm_values_dev_yaml, '__CD_GROUP_NAME__', CI_GROUP_NAME)
            replacement(helm_values_dev_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
            replacement(helm_values_dev_yaml, '__CD_PROJECT_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_dev_yaml, '__CD_APPLICATION_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_dev_yaml, '__CD_HELM_CONTAINER_PORT__', CD_HELM_CONTAINER_PORT)
            replacement(helm_values_dev_yaml, '__CD_HELM_MANAGEMENT_PORT__', CD_HELM_MANAGEMENT_PORT)
            replacement(helm_values_dev_yaml, '__CD_HELM_SERVICE_PORT__', CD_HELM_SERVICE_PORT)
            replacement(helm_values_dev_yaml, '__CD_HELM_DOMAIN_NAME__', CD_HELM_DOMAIN_NAME_DEV)
        elif branch == "master":
            recursive_copy(helm_chart_source_path, helm_chart_destination_path)
            os.rename(helm_chart_destination_path + 'values.yaml', helm_chart_destination_path + branch + ".yaml")
            os.remove(helm_values_dev_yaml)
            replacement(helm_chart_yaml,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_master_yaml,'__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_master_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
            replacement(helm_values_master_yaml, '__CD_GROUP_NAME__', CI_GROUP_NAME)
            replacement(helm_values_master_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
            replacement(helm_values_master_yaml, '__CD_PROJECT_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_master_yaml, '__CD_APPLICATION_NAME__', CI_PROJECT_NAME)
            replacement(helm_values_master_yaml, '__CD_HELM_CONTAINER_PORT__', CD_HELM_CONTAINER_PORT)
            replacement(helm_values_master_yaml, '__CD_HELM_MANAGEMENT_PORT__', CD_HELM_MANAGEMENT_PORT)
            replacement(helm_values_master_yaml, '__CD_HELM_SERVICE_PORT__', CD_HELM_SERVICE_PORT)
            replacement(helm_values_master_yaml, '__CD_HELM_DOMAIN_NAME__', CD_HELM_DOMAIN_NAME_PROD)

        os.system('git add .')
        os.system("git status")
        os.system("git commit -am 'Configured project'")
        os.system("git push --set-upstream origin " + branch)

    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def git_push_to_chart_multi_module(repo_path, branches, helm_chart_yaml, helm_values_dev_yaml, helm_values_master_yaml):
    os.chdir(repo_path)

    if CI_PROJECT_GENERATION == "TRUE":
        MODULES = get_modules(gradle_settings, wordCheck, moduleCheck)
    elif CI_PROJECT_MIGRATION == "TRUE":
        MODULES = CI_PROJECT_MULTI_MODULE_NAMES.split(' ')

    for branch in branches:
        os.system('git checkout -b' + branch)
        for MODULE in MODULES:
            create_folder(MODULE)
            
            helm_chart_yaml = current_directory + '/' + chart_path + "/" + MODULE + '/Chart.yaml'
            helm_values_dev_yaml = current_directory + '/' + chart_path + "/" + MODULE + '/develop.yaml' 
            helm_values_master_yaml = current_directory + '/' + chart_path + "/" + MODULE + '/master.yaml'

            if branch == "develop":
                recursive_copy(helm_chart_source_path, helm_chart_destination_path + "/" + MODULE)
                os.rename(helm_chart_destination_path + "/" + MODULE + "/" + 'values.yaml', helm_chart_destination_path + "/" + MODULE + "/" + branch + ".yaml")
                replacement(helm_chart_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                replacement(helm_values_dev_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                replacement(helm_values_dev_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
                replacement(helm_values_dev_yaml, '__CD_GROUP_NAME__', CI_GROUP_NAME)
                replacement(helm_values_dev_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
                replacement(helm_values_dev_yaml, '__CD_PROJECT_NAME__', CI_PROJECT_NAME + "/" + MODULE)
                replacement(helm_values_dev_yaml, '__CD_APPLICATION_NAME__', MODULE)
                replacement(helm_values_dev_yaml, '__CD_HELM_CONTAINER_PORT__', CD_HELM_CONTAINER_PORT)
                replacement(helm_values_dev_yaml, '__CD_HELM_MANAGEMENT_PORT__', CD_HELM_MANAGEMENT_PORT)
                replacement(helm_values_dev_yaml, '__CD_HELM_SERVICE_PORT__', CD_HELM_SERVICE_PORT)
                replacement(helm_values_dev_yaml, '__CD_HELM_DOMAIN_NAME__', CD_HELM_DOMAIN_NAME_DEV)
            elif branch == "master":
                recursive_copy(helm_chart_source_path, helm_chart_destination_path + "/" + MODULE)
                os.rename(helm_chart_destination_path + "/" + MODULE + "/" + 'values.yaml', helm_chart_destination_path + "/" + MODULE + "/" + branch + ".yaml")
                os.remove(helm_values_dev_yaml)
                replacement(helm_chart_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                replacement(helm_values_master_yaml,'__CD_HELM_CHART_NAME__', MODULE)
                replacement(helm_values_master_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
                replacement(helm_values_master_yaml, '__CD_GROUP_NAME__', CI_GROUP_NAME)
                replacement(helm_values_master_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
                replacement(helm_values_master_yaml, '__CD_PROJECT_NAME__', CI_PROJECT_NAME + "/" + MODULE)
                replacement(helm_values_master_yaml, '__CD_APPLICATION_NAME__', MODULE)
                replacement(helm_values_master_yaml, '__CD_HELM_CONTAINER_PORT__', CD_HELM_CONTAINER_PORT)
                replacement(helm_values_master_yaml, '__CD_HELM_MANAGEMENT_PORT__', CD_HELM_MANAGEMENT_PORT)
                replacement(helm_values_master_yaml, '__CD_HELM_SERVICE_PORT__', CD_HELM_SERVICE_PORT)
                replacement(helm_values_master_yaml, '__CD_HELM_DOMAIN_NAME__', CD_HELM_DOMAIN_NAME_PROD)

        os.system('git add .')
        os.system("git status")
        os.system("git commit -am 'Configured project'")
        os.system("git push --set-upstream origin " + branch)

    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def git_push_to_application(repo_path, branches):
    os.chdir(repo_path)

    create_folder(CI_PROJECT_NAME)

    argo_application_yaml = argo_application_destination_path + CI_PROJECT_NAME + "/" + CI_PROJECT_NAME + "-application.yaml"
    argo_gitlab_ci_yaml = argo_application_destination_path + ".gitlab-ci.yml"

    for branch in branches:
        os.system('git checkout -b' + branch)

        if branch == "develop":
            file_copy(argo_template_source_path + "application-single-module.yaml", argo_application_yaml)
            replacement(argo_application_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
            replacement(argo_application_yaml, '__CD_PROJECT_NAME__', CI_PROJECT_NAME)
            replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            replacement(argo_application_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
            replacement(argo_application_yaml, '__CD_GROUP_NAME__', CD_GROUP_NAME)
            replacement(argo_application_yaml, '__CI_BRANCH_NAME__', branch)

            file_copy(argo_gitlab_ci_application_template, argo_gitlab_ci_yaml)
            replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
            replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)

        if branch == "master":
            file_copy(argo_template_source_path + "application-single-module.yaml", argo_application_yaml)
            replacement(argo_application_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
            replacement(argo_application_yaml, '__CD_PROJECT_NAME__', CI_PROJECT_NAME)
            replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', CI_PROJECT_NAME)
            replacement(argo_application_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
            replacement(argo_application_yaml, '__CD_GROUP_NAME__', CD_GROUP_NAME)
            replacement(argo_application_yaml, '__CI_BRANCH_NAME__', branch)

            file_copy(argo_gitlab_ci_application_template, argo_gitlab_ci_yaml)
            replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
            replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)

        os.system('git add .')
        os.system("git status")
        os.system("git commit -am 'Updated application.yaml'")
        os.system("git push --set-upstream origin " + branch)

    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def git_push_to_application_multi_module(repo_path, branches):
    os.chdir(repo_path)

    create_folder(CI_PROJECT_NAME)

    if CI_PROJECT_GENERATION == "TRUE":
        MODULES = get_modules(gradle_settings, wordCheck, moduleCheck)
    elif CI_PROJECT_MIGRATION == "TRUE":
        MODULES = CI_PROJECT_MULTI_MODULE_NAMES.split(' ')
 
    for branch in branches:
        os.system('git checkout -b' + branch)
        for MODULE in MODULES:
            create_folder(CI_PROJECT_NAME + "/" + MODULE)

            argo_application_yaml = argo_application_destination_path + CI_PROJECT_NAME + "/" + MODULE + "/" + CI_PROJECT_NAME + "-application.yaml"
            argo_gitlab_ci_yaml = argo_application_destination_path + ".gitlab-ci.yml"

            if branch == "develop":
                file_copy(argo_template_source_path + "application-multi-module.yaml", argo_application_yaml)
                replacement(argo_application_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
                replacement(argo_application_yaml, '__CD_PROJECT_NAME__', MODULE)
                replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', MODULE)
                replacement(argo_application_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
                replacement(argo_application_yaml, '__CD_GROUP_NAME__', CD_GROUP_NAME)
                replacement(argo_application_yaml, '__CI_BRANCH_NAME__', branch)
                replacement(argo_application_yaml, '__CI_MODULE_NAME__', MODULE)

                file_copy(argo_gitlab_ci_application_template, argo_gitlab_ci_yaml)
                replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
                replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)

            if branch == "master":
                file_copy(argo_template_source_path + "application-multi-module.yaml", argo_application_yaml)
                replacement(argo_application_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
                replacement(argo_application_yaml, '__CD_PROJECT_NAME__', MODULE)
                replacement(argo_application_yaml, '__CD_HELM_CHART_NAME__', MODULE)
                replacement(argo_application_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)
                replacement(argo_application_yaml, '__CI_BRANCH_NAME__', branch)
                replacement(argo_application_yaml, '__CI_MODULE_NAME__', MODULE)
                replacement(argo_application_yaml, '__CD_GROUP_NAME__', CD_GROUP_NAME)
                file_copy(argo_gitlab_ci_application_template, argo_gitlab_ci_yaml)
                replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
                replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)

        os.system('git add .')
        os.system("git status")
        os.system("git commit -am 'Updated application.yaml'")
        os.system("git push --set-upstream origin " + branch)

    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def git_push_to_project(repo_path):
    os.chdir(repo_path)

    create_folder(CI_SUBGROUP_NAME)

    argo_project_yaml = argo_project_destination_path + CI_SUBGROUP_NAME + "/" + CI_SUBGROUP_NAME + "-project.yaml"
    argo_gitlab_ci_yaml = argo_project_destination_path + ".gitlab-ci.yml"

    branch = "develop"
    os.system('git checkout -b' + branch)

    file_copy(argo_template_source_path + "project.yaml", argo_project_yaml)
    replacement(argo_project_yaml, '__CD_SUBGROUP_NAME__', CI_SUBGROUP_NAME)
    replacement(argo_project_yaml, '__CD_HELM_NAMESPACE__', CD_HELM_NAMESPACE)

    file_copy(argo_gitlab_ci_project_template, argo_gitlab_ci_yaml)
    replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_FRONTEND__', CI_PROJECT_TYPE_FRONTEND)
    replacement(argo_gitlab_ci_yaml, '__CI_PROJECT_TYPE_BACKEND__', CI_PROJECT_TYPE_BACKEND)

    os.system('git add .')
    os.system("git status")
    os.system("git commit -am 'Updated project.yaml'")
    os.system("git push --set-upstream origin " + branch)

    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)

def project_creation():
    gl = connect_gitlab(url=CI_GITLAB_SERVER, private_token=CI_GITLAB_TOKEN, ssl_verify=ssl_verify, api_version="4")

    list_subgroups_id_all = []
    list_subgroups_id_stored = []

    def find_subgroups(group_id):
        group = gl.groups.get(group_id)
        list_subgroups_id = []
        for sub in group.subgroups.list(all=True):
            list_subgroups_id.append(sub.id)
        return(list_subgroups_id)

    def iterate_subgroups(group_id, list_subgroups_id_all):
        list_subgroups_id = find_subgroups(group_id)
        list_subgroups_id_stored.append(list_subgroups_id)
        for subgroup_id in list_subgroups_id:
            if subgroup_id not in list_subgroups_id_all:
                list_subgroups_id_all.append(subgroup_id)
                list_subgroups_id_tmp = iterate_subgroups(subgroup_id, list_subgroups_id_all)
                list_subgroups_id_stored.append(list_subgroups_id_tmp)
        return(list_subgroups_id_all)

    code_list_subgroups_id_all = iterate_subgroups(code_subgroup_id , list_subgroups_id_all)
    chart_list_subgroups_id_all = iterate_subgroups(chart_subgroup_id , list_subgroups_id_all)
    application_list_subgroups_id_all = iterate_subgroups(application_subgroup_id , list_subgroups_id_all)

# ---------------------------------------------------------

    code_list_names = []
    for ids in code_list_subgroups_id_all:
        group = gl.groups.get(ids)
        group_name = group.attributes['name']
        code_list_names.append(group_name)

    if CI_SUBGROUP_NAME in code_list_names:
        print("Group: " + CI_SUBGROUP_NAME + " is exists in " + code_path + " path!")
    else:
        print("Group: " + CI_SUBGROUP_NAME + " is not available in " + code_path + " path, it will be created..")
        code_subgroup = gl.groups.create({"name": CI_SUBGROUP_NAME, "path": CI_SUBGROUP_NAME, 'visibility': visibility, "parent_id": code_subgroup_id})

# ---------------------------------------------------------

    chart_list_names = []
    for ids in chart_list_subgroups_id_all:
        group = gl.groups.get(ids)
        group_name = group.attributes['name']
        chart_list_names.append(group_name)

    if CI_SUBGROUP_NAME in chart_list_names:
        print("Group: " + CI_SUBGROUP_NAME + " is exists in " + chart_path + " path!")
    else:
        print("Group: " + CI_SUBGROUP_NAME + " is not available in " + chart_path + " path, it will be created..")
        chart_subgroup = gl.groups.create({"name": CI_SUBGROUP_NAME, "path": CI_SUBGROUP_NAME, 'visibility': visibility, "parent_id": chart_subgroup_id})

# ---------------------------------------------------------

    application_list_names = []
    for ids in application_list_subgroups_id_all:
        group = gl.groups.get(ids)
        group_name = group.attributes['name']
        application_list_names.append(group_name)

    if CI_SUBGROUP_NAME in application_list_names:
        print("Group: " + CI_SUBGROUP_NAME + " is exists in " + application_path + " path!")
    else:
        print("Group: " + CI_SUBGROUP_NAME + " is not available in " + application_path + " path, it will be created..")
        application_subgroup = gl.groups.create({"name": CI_SUBGROUP_NAME, "path": CI_SUBGROUP_NAME, 'visibility': visibility, "parent_id": application_subgroup_id})

# ---------------------------------------------------------

    list_subgroups_id_all = []
    code_list_subgroups_id_all = iterate_subgroups(code_subgroup_id , list_subgroups_id_all)

    code_new_group_id = ""
    for ids in code_list_subgroups_id_all:
        group = gl.groups.get(ids)
        if CI_SUBGROUP_NAME == group.attributes['name']:
            code_new_group_id = group.attributes['id']

    list_subgroups_id_all = []
    chart_list_subgroups_id_all = iterate_subgroups(chart_subgroup_id , list_subgroups_id_all)

    chart_new_group_id = ""
    for ids in chart_list_subgroups_id_all:
        group = gl.groups.get(ids)
        if CI_SUBGROUP_NAME == group.attributes['name']:
            chart_new_group_id = group.attributes['id']

    list_subgroups_id_all = []
    application_list_subgroups_id_all = iterate_subgroups(application_subgroup_id , list_subgroups_id_all)

    application_new_group_id = ""
    for ids in application_list_subgroups_id_all:
        group = gl.groups.get(ids)
        if CI_SUBGROUP_NAME == group.attributes['name']:
            application_new_group_id = group.attributes['id']

# ------------------------------------------------------

    project_name_with_namespace = f"development/{code_path}/{CI_SUBGROUP_NAME}/{CI_PROJECT_NAME}"
    project_check_exists = ''

    try:
        project_check_exists = gl.projects.get(project_name_with_namespace).name
    except gitlab.exceptions.GitlabGetError:
        print("Project: " + CI_PROJECT_NAME + " is not exists in " + CI_SUBGROUP_NAME + " subgroup on " + code_path + " path!")

    if CI_PROJECT_NAME == project_check_exists:
        print("Project: " + CI_PROJECT_NAME + " already exists in " + CI_SUBGROUP_NAME + " subgroup on " + code_path + " path!")
        sys.exit("A Project with the same name under the subgroup cannot be created again")
    else:
        print("Project: " + CI_PROJECT_NAME + " will be created in " + CI_SUBGROUP_NAME + " subgroup on " + code_path + " path..")
        code_group_project = gl.projects.create({'name': CI_PROJECT_NAME, 'visibility': visibility, 'namespace_id': code_new_group_id})

    project_name_with_namespace = f"development/{chart_path}/{CI_SUBGROUP_NAME}/{CI_PROJECT_NAME}"
    project_check_exists = ''

    try:
        project_check_exists = gl.projects.get(project_name_with_namespace).name
    except gitlab.exceptions.GitlabGetError:
        print("Project: " + CI_PROJECT_NAME + " is not exists in " + CI_SUBGROUP_NAME + " subgroup on " + chart_path + " path!")

    if CI_PROJECT_NAME == project_check_exists:
        print("Project: " + CI_PROJECT_NAME + " already exists in " + CI_SUBGROUP_NAME + " subgroup on " + chart_path + " path!")
        sys.exit("A Project with the same name under the subgroup cannot be created again")
    else:
        print("Project: " + CI_PROJECT_NAME + " will be created in " + CI_SUBGROUP_NAME + " subgroup on " + chart_path + " path..")
        chart_group_project = gl.projects.create({'name': CI_PROJECT_NAME, 'visibility': visibility, 'namespace_id': chart_new_group_id})

    project_name_with_namespace = f"development/{application_path}/{CI_SUBGROUP_NAME}/{CI_PROJECT_NAME}"
    project_check_exists = ''

    try:
        project_check_exists = gl.projects.get(project_name_with_namespace).name
    except gitlab.exceptions.GitlabGetError:
        print("Project: " + CI_PROJECT_NAME + " is not exists in " + CI_SUBGROUP_NAME + " subgroup on " + application_path + " path!")

    if CI_PROJECT_NAME == project_check_exists:
        print("Project: " + CI_PROJECT_NAME + " already exists in " + CI_SUBGROUP_NAME + " subgroup on " + application_path + " path!")
        sys.exit("A Project with the same name under the subgroup cannot be created again")
    else:
        print("Project: " + CI_PROJECT_NAME + " will be created in " + CI_SUBGROUP_NAME + " subgroup on " + application_path + " path..")
        application_group_project = gl.projects.create({'name': CI_PROJECT_NAME, 'visibility': visibility, 'namespace_id': application_new_group_id})

    project_name_with_namespace = f"development/{project_path}/{CI_SUBGROUP_NAME}"
    project_check_exists = ''

    try:
        project_check_exists = gl.projects.get(project_name_with_namespace).name
    except gitlab.exceptions.GitlabGetError:
        print("Project: " + CI_SUBGROUP_NAME + " is not exists in " + project_path + " path!")

    if CI_SUBGROUP_NAME == project_check_exists:
        PROJECT_EXISTS = True
        print("Project: " + CI_SUBGROUP_NAME + " already exists in " + project_path + " path!")
    else:
        print("Project: " + CI_SUBGROUP_NAME + " will be created in " + project_path + " path..")
        try:
            project_group_project = gl.projects.create({'name': CI_SUBGROUP_NAME, 'visibility': visibility, 'namespace_id': project_subgroup_id})
        except gitlab.exceptions.GitlabCreateError:
            print("A Project with the same name under the group cannot be created again")

def git_clone_repositories():
    create_folder(helm_chart_path)
    delete_folder(helm_chart_path)
    os.system("git clone https://" + CI_GITLAB_TOKEN_NAME + ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/devops/cicd-template" + "/" + helm_chart_path + ".git ./" + helm_chart_path)
    delete_folder(helm_chart_source_path + ".git")
    
    create_folder(gitlab_ci_path)
    delete_folder(gitlab_ci_path)
    os.system("git clone https://" + CI_GITLAB_TOKEN_NAME + ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/devops/cicd-template" + "/" + gitlab_ci_path + ".git ./" + gitlab_ci_path)
    delete_folder(gitlab_ci_source_path + ".git")

    if CI_PROJECT_GENERATION == "TRUE" and CI_PROJECT_MODE_MONO_REPO == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
        create_folder(gradle_single_module_path)
        delete_folder(gradle_single_module_path)
        os.system("git clone https://"  + CI_GITLAB_TOKEN_NAME +  ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/devops/cicd-template" + "/" + gradle_single_module_path + ".git ./" + gradle_single_module_path)
        delete_folder(project_gradle_single_module_source_path + ".git")
    elif CI_PROJECT_GENERATION == "TRUE" and CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
        create_folder(gradle_multi_module_path)
        delete_folder(gradle_multi_module_path)
        os.system("git clone https://"  + CI_GITLAB_TOKEN_NAME +  ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/devops/cicd-template" + "/" + gradle_multi_module_path + ".git ./" + gradle_multi_module_path)
        delete_folder(project_gradle_multi_module_source_path + ".git")

    create_folder(argo_template_path)
    delete_folder(argo_template_path)
    os.system("git clone https://"  + CI_GITLAB_TOKEN_NAME +  ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/devops/cicd-template" + "/" + argo_template_path + ".git ./" + argo_template_path)
    delete_folder(argo_template_source_path + ".git")

    create_folder(code_path)
    delete_folder(code_path)
    os.system("git clone https://"  + CI_GITLAB_TOKEN_NAME +  ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/development/" + code_path + "/" + CI_SUBGROUP_NAME + "/" + CI_PROJECT_NAME + ".git ./" + code_path)
    
    create_folder(chart_path)
    delete_folder(chart_path)
    os.system("git clone https://" + CI_GITLAB_TOKEN_NAME + ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/development/" + chart_path + "/" + CI_SUBGROUP_NAME + "/" + CI_PROJECT_NAME + ".git ./" + chart_path)

    create_folder(application_path)
    delete_folder(application_path)
    os.system("git clone https://" + CI_GITLAB_TOKEN_NAME + ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/development/" + application_path + "/" + CI_SUBGROUP_NAME + "/" + CI_PROJECT_NAME + ".git ./" + application_path)

    if not PROJECT_EXISTS:
        create_folder(project_path)
        delete_folder(project_path)
        os.system("git clone https://" + CI_GITLAB_TOKEN_NAME + ":" + CI_GITLAB_TOKEN + "@gitlab.local.az/development/" + project_path + "/" + CI_SUBGROUP_NAME + ".git ./" + project_path)


def argo_join_repository(argo_server, argo_username, argo_password, gitlab_username, gitlab_password):
    os.system('argocd login ' + argo_server + ' --insecure --username ' + argo_username + ' --password ' + argo_password)
    os.system("argocd repo add https://gitlab.local.az/development/" + chart_path + "/" + CI_SUBGROUP_NAME + "/" + CI_PROJECT_NAME + ".git --username " + gitlab_username + " --password " + gitlab_password + " --insecure-skip-server-verification")

def main():

    # Checking Environment Variables
    if CI_PROJECT_GENERATION == CI_PROJECT_MIGRATION:
        print(CI_PROJECT_GENERATION + " and " + CI_PROJECT_MIGRATION + " must not be same. Process killed!")
        sys.exit(1)
    elif CI_PROJECT_TYPE_FRONTEND == CI_PROJECT_TYPE_BACKEND:
        print(CI_PROJECT_TYPE_FRONTEND + " and " + CI_PROJECT_TYPE_BACKEND + " must not be same. Process killed!")
        sys.exit(1)
    elif CI_PROJECT_MODE_MONO_REPO == CI_PROJECT_MODE_MULTI_MODULE:
        print(CI_PROJECT_MODE_MONO_REPO + " and " + CI_PROJECT_MODE_MULTI_MODULE + " must not be same. Process killed!")
        sys.exit(1)
    elif CI_APPLICATION_TYPE_MAVEN == "TRUE" and CI_APPLICATION_TYPE_GRADLE == "TRUE":
        print(CI_APPLICATION_TYPE_MAVEN + " and " + CI_APPLICATION_TYPE_GRADLE + " must not be 'TRUE' in same time. Process killed!")
        sys.exit(1)
    elif CI_RELEASE_TYPE_JIB == CI_RELEASE_TYPE_KANIKO:
        print(CI_RELEASE_TYPE_JIB + " and " + CI_RELEASE_TYPE_KANIKO + " must not be same. Process killed!")
        sys.exit(1)

    # Creating groups and projects if not exists
    project_creation()

    # Clone repositories
    git_clone_repositories()

    git_push_to_code(code_path, branches, gitlab_ci_yaml)

    if CI_PROJECT_TYPE_BACKEND == "TRUE" and CI_PROJECT_MODE_MONO_REPO == "TRUE":
        git_push_to_chart(chart_path, branches, helm_chart_yaml, helm_values_dev_yaml, helm_values_master_yaml)
    elif CI_PROJECT_TYPE_BACKEND == "TRUE" and CI_PROJECT_MODE_MULTI_MODULE == "TRUE":
        git_push_to_chart_multi_module(chart_path, branches, helm_chart_yaml, helm_values_dev_yaml, helm_values_master_yaml)

    if CI_PROJECT_TYPE_BACKEND == "TRUE":
        argo_join_repository(CI_ARGO_SERVER_DEV, CI_ARGO_USERNAME_DEV, CI_ARGO_PASSWORD_DEV, CI_ARGO_GITLAB_USERNAME, CI_ARGO_GITLAB_PASSWORD)
        argo_join_repository(CI_ARGO_SERVER_PROD, CI_ARGO_USERNAME_PROD, CI_ARGO_PASSWORD_PROD, CI_ARGO_GITLAB_USERNAME, CI_ARGO_GITLAB_PASSWORD)
    elif CI_PROJECT_TYPE_FRONTEND == "TRUE":
        argo_join_repository(CI_ARGO_SERVER_DEVDMZ, CI_ARGO_USERNAME_DEVDMZ, CI_ARGO_PASSWORD_DEVDMZ, CI_ARGO_GITLAB_USERNAME, CI_ARGO_GITLAB_PASSWORD)
        argo_join_repository(CI_ARGO_SERVER_PRODDMZ, CI_ARGO_USERNAME_PRODDMZ, CI_ARGO_PASSWORD_PRODDMZ, CI_ARGO_GITLAB_USERNAME, CI_ARGO_GITLAB_PASSWORD)

    if not PROJECT_EXISTS:
        git_push_to_project(argo_project_path)

    if CI_PROJECT_MODE_MONO_REPO == "TRUE":
        git_push_to_application(argo_application_path, branches)
    elif CI_PROJECT_MODE_MULTI_MODULE == "TRUE":
        git_push_to_application_multi_module(argo_application_path, branches)


if __name__ == '__main__':
    main()
