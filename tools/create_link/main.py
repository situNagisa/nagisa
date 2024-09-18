import os
import platform
import sys


class VCXProject(object):

    def __init__(self, abs_path):
        self._abs_path = abs_path

    def root(self):
        return self._abs_path

    def project_name(self):
        return os.path.basename(self._abs_path)

    def include_root_dir(self):
        return os.path.join(self._abs_path, 'include/nagisa')

    def include_dirs(self):
        include_dirs = []
        for dir_path, dir_names, filenames in os.walk(self.include_root_dir()):
            if os.path.basename(dir_path) == self.project_name():
                include_dirs.append(dir_path)

        return include_dirs


def create_link(src, dest):
    system = platform.system()

    try:
        os.symlink(src, dest)
        print(f"硬链接创建成功: {dest} -> {src}")
    except Exception as e:
        print(f"创建硬链接失败: {e}")


def find_vcx_project(root_folder):
    vcx_projects = []

    for dir_path, dir_names, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.vcxproj'):
                vcx_projects.append(VCXProject(os.path.abspath(dir_path)))
                break  # 找到一个.vcxproj文件即可，不需要继续检查其他文件

    return vcx_projects


def main():
    target_root_dir = os.path.abspath('../../include/nagisa')
    submodule_root_dirs = os.path.abspath('../../submodules')
    if len(sys.argv) == 3:
        target_root_dir = os.path.abspath(sys.argv[1])
        submodule_root_dirs = os.path.abspath(sys.argv[2])

    # ok = input(f"this operation will delete all files in {target_root_dir}, ok?[y/n]")
    # if ok == 'n':
    #     return

    vcxproj_folders = find_vcx_project(submodule_root_dirs)
    print([proj.project_name() for proj in vcxproj_folders])
    for vcxproj in vcxproj_folders:
        include_dirs = vcxproj.include_dirs()
        if len(include_dirs) == 0:
            print(f"the project {vcxproj.project_name()} has no include dir")
            continue
        if len(include_dirs) > 1:
            print(f"the project {vcxproj.project_name()} has multiple include")
        for include_dir in include_dirs:
            parent_dir = os.path.join(target_root_dir,
                                      os.path.dirname(os.path.relpath(include_dir, vcxproj.include_root_dir())))
            os.makedirs(parent_dir, exist_ok=True)
            create_link(os.path.abspath(include_dir), os.path.join(parent_dir, vcxproj.project_name()))

if __name__ == '__main__':
    main()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
