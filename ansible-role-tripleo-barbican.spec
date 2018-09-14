%global srcname ansible_role_tripleo_barbican
%global rolename ansible-role-tripleo-barbican

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           %{rolename}
Version: 0.0.1.dev1
Release: 99999
Summary:        Ansible Barbican role for the TripleO project

Group:          System Environment/Base
License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/ansible-role-tripleo-barbican
Source0: ansible-role-tripleo-zaqar-master.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python-d2to1
BuildRequires:  python2-pbr

Requires: ansible

%description

Ansible Barbican role for the TripleO project

%prep
%autosetup -n %{rolename}-%{upstream_version} -S git


%build
%py2_build


%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%py2_install


%files
%doc README*
%license LICENSE
%{python2_sitelib}/%{srcname}-*.egg-info
%{_datadir}/ansible/roles/


%changelog


