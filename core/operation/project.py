from core.authentication.authentication import GitlabAuth
from gitlab import exceptions, REPORTER_ACCESS, DEVELOPER_ACCESS, MAINTAINER_ACCESS
from core.configuration.variables import GitlabAuthConf, PathConf, GitlabEnvConf, ContainerExprPolicy
from core.operation.command import Command
from sys import exit
from os import system

class GitlabProjOps():
    gitlab_auth      = GitlabAuth()
    gitlab_auth_conf = GitlabAuthConf()
    path             = PathConf()
    gitlab_env       = GitlabEnvConf()
    cmd              = Command()
    policy           = ContainerExprPolicy()

    MODULE                   = ""
    code_new_group_id        = ""
    chart_new_group_id       = ""
    application_new_group_id = ""

    reporters   = cmd.convert_to_list(gitlab_env.CI_ACCESS_REPORTER)
    deveopers   = cmd.convert_to_list(gitlab_env.CI_ACCESS_DEVELOPER)
    maintainers = cmd.convert_to_list(gitlab_env.CI_ACCESS_MAINTAINER)

    gl = gitlab_auth.connect(gitlab_auth_conf.CI_GITLAB_SSL_VERIFY, 
                        gitlab_auth_conf.CI_GITLAB_SERVER, 
                        gitlab_auth_conf.CI_GITLAB_TOKEN, 
                        gitlab_auth_conf.CI_GITLAB_API_VERSION)

    """
    Functions to check the existence of subgroups within the group
    """
    def find_subgroups(self, group_id):
        self.group_id = group_id

        group = self.gl.groups.get(self.group_id)
        list_subgroups_id = []
        for sub in group.subgroups.list(all=True):
            list_subgroups_id.append(sub.id)
        return(list_subgroups_id)

    def iterate_subgroups(self, group_id, list_subgroups_id_all):
        self.group_id = group_id
        self.list_subgroups_id_all = list_subgroups_id_all

        list_subgroups_id_stored = []

        list_subgroups_id = self.find_subgroups(self.group_id)
        list_subgroups_id_stored.append(list_subgroups_id)
        for subgroup_id in list_subgroups_id:
            if subgroup_id not in self.list_subgroups_id_all:
                self.list_subgroups_id_all.append(subgroup_id)
                list_subgroups_id_tmp = self.iterate_subgroups(subgroup_id, self.list_subgroups_id_all)
                list_subgroups_id_stored.append(list_subgroups_id_tmp)
        return(self.list_subgroups_id_all)

    """
    Creation subgroups and projects if is not exists
    """
    def create_groups(self):
        """
        Creation subgroup for Code Group
        ------------------------------------------------------------------------------------------          
        """
        list_subgroups_id_all = []
        code_list_subgroups_id_all = self.iterate_subgroups(self.gitlab_env.code_subgroup_id , list_subgroups_id_all)

        code_list_names = []
        for ids in code_list_subgroups_id_all:
            group = self.gl.groups.get(ids)
            group_name = group.attributes['name']
            code_list_names.append(group_name)

        if self.gitlab_env.CI_SUBGROUP_NAME in code_list_names:
            print("".join(["Group: ", self.gitlab_env.CI_SUBGROUP_NAME, " is exists in ", self.path.code_path, " path!"]))
        else:
            print("".join(["Group: ", self.gitlab_env.CI_SUBGROUP_NAME, " is not available in ", self.path.code_path, " path, it will be created.."]))
            code_subgroup = self.gl.groups.create({"name": self.gitlab_env.CI_SUBGROUP_NAME, 
                                                   "path": self.gitlab_env.CI_SUBGROUP_NAME, 
                                                   'visibility': self.gitlab_env.visibility, 
                                                   "parent_id": self.gitlab_env.code_subgroup_id})
            
        list_subgroups_id_all = []
        code_list_subgroups_id_all = self.iterate_subgroups(self.gitlab_env.code_subgroup_id , list_subgroups_id_all)

        for ids in code_list_subgroups_id_all:
            group = self.gl.groups.get(ids)
            if self.gitlab_env.CI_SUBGROUP_NAME == group.attributes['name']:
                self.code_new_group_id = group.attributes['id']
        
        """
        Creation subgroup for Chart Group    
        ------------------------------------------------------------------------------------------         
        """
        list_subgroups_id_all = []
        chart_list_subgroups_id_all = self.iterate_subgroups(self.gitlab_env.chart_subgroup_id , list_subgroups_id_all)

        chart_list_names = []
        for ids in chart_list_subgroups_id_all:
            group = self.gl.groups.get(ids)
            group_name = group.attributes['name']
            chart_list_names.append(group_name)

        if self.gitlab_env.CI_SUBGROUP_NAME in chart_list_names:
            print("Group: " + self.gitlab_env.CI_SUBGROUP_NAME + " is exists in " + self.path.chart_path + " path!")
        else:
            print("".join(["Group: ", self.gitlab_env.CI_SUBGROUP_NAME, " is not available in ", self.path.chart_path, " path, it will be created.."]))
            chart_subgroup = self.gl.groups.create({"name": self.gitlab_env.CI_SUBGROUP_NAME, 
                                                "path": self.gitlab_env.CI_SUBGROUP_NAME, 
                                                'visibility': self.gitlab_env.visibility, 
                                                "parent_id": self.gitlab_env.chart_subgroup_id})

        list_subgroups_id_all = []
        chart_list_subgroups_id_all = self.iterate_subgroups(self.gitlab_env.chart_subgroup_id, list_subgroups_id_all)

        for ids in chart_list_subgroups_id_all:
            group = self.gl.groups.get(ids)
            if self.gitlab_env.CI_SUBGROUP_NAME == group.attributes['name']:
                self.chart_new_group_id = group.attributes['id']

        """
        Creation subgroup for Argo application Group   
        ------------------------------------------------------------------------------------------ 
        """
        list_subgroups_id_all = []
        application_list_subgroups_id_all = self.iterate_subgroups(self.gitlab_env.application_subgroup_id , list_subgroups_id_all)

        application_list_names = []
        for ids in application_list_subgroups_id_all:
            group = self.gl.groups.get(ids)
            group_name = group.attributes['name']
            application_list_names.append(group_name)

        if self.gitlab_env.CI_SUBGROUP_NAME in application_list_names:
            print("Group: " + self.gitlab_env.CI_SUBGROUP_NAME + " is exists in " + self.path.application_path + " path!")
        else:
            print("".join(["Group: ", self.gitlab_env.CI_SUBGROUP_NAME, " is not available in ", self.path.application_path, " path, it will be created.."]))
            application_subgroup = self.gl.groups.create({"name": self.gitlab_env.CI_SUBGROUP_NAME, 
                                                          "path": self.gitlab_env.CI_SUBGROUP_NAME, 
                                                          'visibility': self.gitlab_env.visibility, 
                                                          "parent_id": self.gitlab_env.application_subgroup_id})

        list_subgroups_id_all = []
        application_list_subgroups_id_all = self.iterate_subgroups(self.gitlab_env.application_subgroup_id, list_subgroups_id_all)

        for ids in application_list_subgroups_id_all:
            group = self.gl.groups.get(ids)
            if self.gitlab_env.CI_SUBGROUP_NAME == group.attributes['name']:
                self.application_new_group_id = group.attributes['id']

    def create_projects(self):
        """
        Creation project for Code Group     
        ------------------------------------------------------------------------------------------        
        """
        project_name_with_namespace = f"{self.gitlab_env.CI_MAIN_GROUP}/{self.path.code_path}/{self.gitlab_env.CI_SUBGROUP_NAME}/{self.gitlab_env.CI_PROJECT_NAME}"
        project_check_exists = ''

        try:
            project_check_exists = self.gl.projects.get(project_name_with_namespace).name
        except exceptions.GitlabGetError:
            print("".join(["Project: ", self.gitlab_env.CI_PROJECT_NAME, " is not exists in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.code_path, " path!"]))
            
        if self.gitlab_env.CI_PROJECT_NAME == project_check_exists:
            print("".join(["Project: ", self.gitlab_env.CI_PROJECT_NAME, " already exists in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.code_path, " path!"]))
        else:
            print("".join(["Project: ", self.gitlab_env.CI_PROJECT_NAME, " will be created in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.code_path, " path.."]))
            code_subgroup_project = self.gl.projects.create({
                            'name': self.gitlab_env.CI_PROJECT_NAME, 
                            'visibility': self.gitlab_env.visibility, 
                            'namespace_id': self.code_new_group_id,
                            'container_expiration_policy_attributes':
                                        {"enabled": self.policy.ENABLED,
                                        "cadence": self.policy.TIME_CLEANUP,
                                        "keep_n": self.policy.TAGS_COUNT_KEEP,
                                        "name_regex_keep": self.policy.NAME_REGEX_KEEP,
                                        "older_than": self.policy.TIME_TAGS_DELETE,
                                        "name_regex": self.policy.NAME_REGEX_DELETE}
                            })
            develop_branch = code_subgroup_project.protectedbranches.create({
                            'name': 'develop',
                            'merge_access_level': DEVELOPER_ACCESS,
                            'push_access_level': MAINTAINER_ACCESS
                            })
            master_branch = code_subgroup_project.protectedbranches.create({
                            'name': 'master',
                            'merge_access_level': DEVELOPER_ACCESS,
                            'push_access_level': MAINTAINER_ACCESS
                            })

            for maintainer in self.maintainers:
                try:
                    user = self.gl.users.list(username=maintainer)[0]
                    access = code_subgroup_project.members.create({'user_id': user.id, 'access_level': MAINTAINER_ACCESS})
                except IndexError:
                    print(maintainer + " for maintainer access is not available")
            for developer in self.deveopers:
                try:
                    user = self.gl.users.list(username=developer)[0]
                    access = code_subgroup_project.members.create({'user_id': user.id, 'access_level': DEVELOPER_ACCESS})
                except IndexError:
                    print(developer + " for developer access is not available")

        """
        Creation project for Chart Group 
        ------------------------------------------------------------------------------------------           
        """

        if self.gitlab_env.CI_PROJECT_MODE_MULTI_MODULE == "TRUE" and self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE != "NULL":
            self.MODULE = self.gitlab_env.CI_PROJECT_MODULE_NAME_FOR_MULTI_MDOULE
        else:
            self.MODULE = self.gitlab_env.CI_PROJECT_NAME

        project_name_with_namespace = f"{self.gitlab_env.CI_MAIN_GROUP}/{self.path.chart_path}/{self.gitlab_env.CI_SUBGROUP_NAME}/{self.MODULE}"
        project_check_exists = ''

        try:
            project_check_exists = self.gl.projects.get(project_name_with_namespace).name
        except exceptions.GitlabGetError:
            print("".join(["Project: ", self.MODULE, " is not exists in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.chart_path, " path!"]))

        if self.MODULE == project_check_exists:
            print("".join(["Project: ", self.MODULE, " already exists in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.chart_path, " path!"]))
        else:
            print("".join(["Project: ", self.MODULE, " will be created in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.chart_path, " path.."]))
            chart_subgroup_project = self.gl.projects.create({
                                'name': self.MODULE, 
                                'visibility': self.gitlab_env.visibility, 
                                'namespace_id': self.chart_new_group_id
                                })
            develop_branch = chart_subgroup_project.protectedbranches.create({
                            'name': 'develop',
                            'merge_access_level': DEVELOPER_ACCESS,
                            'push_access_level': MAINTAINER_ACCESS
                            })
            master_branch = chart_subgroup_project.protectedbranches.create({
                            'name': 'master',
                            'merge_access_level': DEVELOPER_ACCESS,
                            'push_access_level': MAINTAINER_ACCESS
                            })

            for maintainer in self.maintainers:
                try:
                    user = self.gl.users.list(username=maintainer)[0]
                    access = chart_subgroup_project.members.create({'user_id': user.id, 'access_level': MAINTAINER_ACCESS})
                except IndexError:
                    print(maintainer + " for maintainer access is not available")
            for developer in self.deveopers:
                try:
                    user = self.gl.users.list(username=developer)[0]
                    access = chart_subgroup_project.members.create({'user_id': user.id, 'access_level': DEVELOPER_ACCESS})
                except IndexError:
                    print(developer + " for developer access is not available")

        """
        Creation project for Argo Application Group
        ------------------------------------------------------------------------------------------           
        """        
        project_name_with_namespace = f"{self.gitlab_env.CI_MAIN_GROUP}/{self.path.application_path}/{self.gitlab_env.CI_SUBGROUP_NAME}/{self.MODULE}"
        project_check_exists = ''

        try:
            project_check_exists = self.gl.projects.get(project_name_with_namespace).name
        except exceptions.GitlabGetError:
            print("".join(["Project: ", self.MODULE, " is not exists in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.application_path, " path!"]))

        if self.MODULE == project_check_exists:
            print("".join(["Project: ", self.MODULE, " already exists in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.application_path, " path!"]))
            exit("A Project with the same name under the subgroup cannot be created again")
        else:
            print("".join(["Project: ", self.MODULE, " will be created in ", self.gitlab_env.CI_SUBGROUP_NAME, " subgroup on ", self.path.application_path, " path!"]))
            argo_application_subgroup_project = self.gl.projects.create({
                            'name': self.MODULE, 
                            'visibility': self.gitlab_env.visibility, 
                            'namespace_id': self.application_new_group_id
                            })
        
        """
        Creation project for Argo Project Group  
        ------------------------------------------------------------------------------------------      
        """
        project_name_with_namespace = f"{self.gitlab_env.CI_MAIN_GROUP}/{self.path.project_path}/{self.gitlab_env.CI_SUBGROUP_NAME}"
        project_check_exists = ''
        PROJECT_EXISTS = False

        try:
            project_check_exists = self.gl.projects.get(project_name_with_namespace).name
            PROJECT_EXISTS = True
        except exceptions.GitlabGetError:
            print("".join(["Project: ", self.gitlab_env.CI_SUBGROUP_NAME, " is not exists in ", self.path.project_path, " path!"]))

        if self.gitlab_env.CI_SUBGROUP_NAME == project_check_exists:
            print("".join(["Project: ", self.gitlab_env.CI_SUBGROUP_NAME, " already exists in ", self.path.project_path, " path!"]))
        else:
            print("".join(["Project: ", self.gitlab_env.CI_SUBGROUP_NAME, " will be created in ", self.path.project_path, " path.."]))
            try:
                if PROJECT_EXISTS == False:
                    argo_project_subgroup_project = self.gl.projects.create({
                                'name': self.gitlab_env.CI_SUBGROUP_NAME, 
                                'visibility': self.gitlab_env.visibility, 
                                'namespace_id': self.gitlab_env.project_subgroup_id})
                else:
                    print("Project for ArgoProj is already exists!")
            except exceptions.GitlabCreateError:
                print("A Project with the same name under the group cannot be created again")


        """
        Granting reporter access to the Images and CI-template subgroups under the DevOps group
        ------------------------------------------------------------------------------------------
        """
        for reporter in self.reporters:
            try:
                user = self.gl.users.list(username=reporter)[0]
                group = self.gl.groups.get(self.gitlab_env.CI_IMAGE_REPO_ID, lazy=True)
                group_access = group.members.create({'user_id': user.id, 'access_level': REPORTER_ACCESS})
                project = self.gl.projects.get(self.gitlab_env.CI_IMAGE_REPO_ID,  lazy=True)
                project_access = project.members.create({'user_id': user.id, 'access_level': REPORTER_ACCESS})       
            except IndexError:
                print(reporter + " for reporter access is not available")
            except exceptions.GitlabCreateError:
                print("User already exists!")
