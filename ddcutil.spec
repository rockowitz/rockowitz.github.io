Name: ddcutil
Version: 0.8.0

# %%{echo:"?????????????????????????????????????????????????????????????????????????????????"}

# So here's the problem: 
# We'd like to include in the package filename an indication of the distribution being built for. 
# Otherwise, packages built for different distributions can have the same filename, making it 
# easy to use the wrong file when installing a package.  

# Some distributions include a distribution string.  Examples:
# Fedora: coreutils-8.25-4.fc24.x86_64.rpm
# Mageia: coreutils-8.25-1.mga6.x86_64.rpm
# CentOS: coreutils-5.97-34.el5_8.1.x86_64.rpm (CentOS 5.11)
#
# Some distributions do not include a distribution string: 
# openSUSE: coreutils-8.23-2.12.1.x86_64.rpm (openSUSE 13.2)
# 
# Mandravia does it both ways
# Mandravia: coreutils-8.12.1-2.x86_64.rpm   (Mandravia 2011)
# Mandravia: coreutils-7.5-2.1mdv2010.0.x86_64.rpm (Mandravia 2010)
#
# Constraints on a solution: 
#
# OBS replaces the Release: tag in the spec file with its own value.  
# By default, this is Release: <CI_CNT>.<B_CNT>
# This can be overridden in the prjconf file 
# 
# Various macros may or may not exist depending on whether the package is being 
# built locally or under OBS, and depending on the target OS. 
#
# The following files are not installed by OBS: 
#   /etc/os-release
#   /etc/fedora-release
#   /etc/SuSE-release     
# 


# Release: tag template specified in prjconf: 
# Release: <CI_CNT>.<B_CNT>%%{?release_suffix}

# Inventory of interesting predefined macros goes here


# Detect if executing under OBS 
# Documentation (https://en.opensuse.org/openSUSE:Build_Service_Tips_and_Tricks#List_available_packages_in_a_distro) 
# states that macro %%opensuse_bs is defined for OBS builds.  
# However, as observed: 
#     it is defined if building for suse 
#     it is not defined if building for fedora
# Instead, test for macro %%{disturl}, which is defined on the command in OBS invoking rpmbuild 
# TODO: add check that disturl starts with obs:

%define is_obs_build %{defined disturl}

# These macros will work on local builds, but not on OBS builds because the files being checked do not exist. 
%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)
%define is_suse   %(test -e /etc/SuSE-release && echo 1 || echo 0)
# release number with periods removed
%define distver %(release="`rpm -q --whatprovides /etc/os-release --queryformat='%{VERSION}' 2> /dev/null | tr . : | sed s/://g`" ; if test $? != 0 ; then release="" ; fi ; echo "$release")
%define osid %(grep "^ID=" /etc/os-release | sed s/ID=//)
%define osversionid %(grep "^VERSION_ID=" /etc/os-release | sed s/VERSION_ID=// | tr -d \"\")

# Defined on: Fedora (local), Ubuntu (local), not defined Fedora (OBS)
%define lsb_release %(lsb_release -r -s)

# Get following message (also or line for suse) but seems to work
# Warning: spec file parser line 69: can't expand %%(...)
%define any_fedora %{expand: %{is_fedora} || 0%{?fedora_version}}
%if %{is_fedora} || 0%{?fedora_version} 
  %define any_fedora 1
%else 
  %define any_fedora 0
%endif
%define any_suse %{expand: %{is_suse} || 0%{?suse_version}}
%if %{is_suse} || 0%{?suse_version} 
  %define any_suse 1
%else 
  %define any_suse 0
%endif

#define any_suse2 0
%if %{is_suse} 
  %define any_suse2 1
%endif


# Inventory of our macros goes here
%{echo:is_obs_build is %{?is_obs_build}, }
%{echo:is_fedora    is %{?is_fedora}, }
%{echo:is_suse      is %{?is_suse}, }
%{echo:any_fedora   is %{?any_fedora}, }
%{echo:any_suse     is %{?any_suse}, }
%{echo:any_suse2    is %{?any_suse2}, }

%{echo:suse_version is %{?suse_version}, }
# ?leap version is documented at https://en.opensuse.org/openSUSE:Build_Service_cross_distribution_howto
# but in fact does not appear to be set
# %%{echo:leap_version is %%{?leap_version}, }
%{echo:sle_version  is %{?sle_version}, }


%if %{is_obs_build}
   %{echo:Executing in Open Build Service, }
   %if 0%{?suse_version}
      %define release_suffix .suse_%{suse_version}
   %endif
   %if 0%{?fedora_version}
      %define release_suffix .fc%{fedora_version}
   %endif
%else
   %{echo:Not an Open Build Service build, }
   %if %{defined dist}
      %{echo:dist IS defined, }
      %define distro %{dist}
      %{echo: distro(a) is %{?distro}, }
   %else 
      %{echo:dist IS NOT defined, }
      %define distro .%{osid}%{osversionid}
      %if 0%{?fedora}
         # should never happen, dist should be defined
         %{echo: case fedora, }
         %define distro .fb%{fedora}
      %endif
      %if 0%{?suse_version}
         %{echo: case  suse_version, }
         # suse_version is 1230 when building on 13.1! 
         # %%define distro .susb%%{suse_version}
         %define distro .suse_%{distver}
      %endif

   %endif
   %{echo: distro(b) is %{?distro}, }
%endif


# %%dump
# will be replaced with version from prjdata if running in OBS 
%{echo: distro(c) is %{?distro}, }
Release: 1%{?distro}
%{echo:"==================================================================="}

# will be 0 or 1:
%define build_libs 1
%define use_usb 1

%if %{build_libs} == 1
%{echo: =================================> defining _unpackaged_files_terminate_build 0, }
# laclient is built but not packaged, avoid termination
%define _unpackaged_files_terminate_build 0 
%endif




Summary: Query and update monitor settings
%if %{defined fedora}
License: GPLv2+
%endif
%if %{defined suse_version}
License: GPL-2.0+
%endif

URL: http://github.com/rockowitz/ddctool
# BuildRequires: gcc  glib2 glib2-devel 
BuildRequires: gcc  pkgconfig(glib-2.0) i2c-tools libXrandr-devel
BuildRequires: libdrm-devel

%if %{defined fedora}
BuildRequires: python2-devel
%endif
%if %{defined suse_version}
BuildRequires: python-devel
%endif

# Works on Fedora, fails on OBS with message 
# "nothing provides libudev-devel, nothing provides or, nothing provides systemd-devel", 
# whether or not a version is included
# BuildRequires: (libudev-devel or systemd-devel)
# BuildRequires: libudev-devel >= 1 or systemd-devel >= 200
%if %{use_usb} == 1
# FIXME: package for udev depends on OS.  Fedora requires systemd-devel, suse still has udev in libudev-devel
%if %{defined fedora}
BuildRequires: libusbx-devel
BuildRequires: systemd-devel
BuildRequires: zlib zlib-devel
%endif
%if %{defined suse_version}
BuildRequires: libusb-1_0-devel
BuildRequires: libudev-devel
BuildRequires: libz1 zlib-devel 
# BuildRequires: zlib-devel-static
# temporarily disable rpmlint after build - will this prevent failure?
# BuildRequires: -post-build-checks
%endif
%endif

# OBS complains for SuSE:
# ddctool.x86_64: W: explicit-lib-dependency glib2
# ddctool.x86_64: W: explicit-lib-dependency libXrandr
# ddctool.x86_64: W: explicit-lib-dependency libdrm2
# You must let rpm find the library dependencies by itself. Do not put unneeded
# explicit Requires: tags.
# %%if %%{defined suse_version}
Requires: i2c-tools 
# %%else
# Requires: i2c-tools 
# Requires: glib2 libXrandr
# %%endif

Source: %{name}-%{version}.tar.gz

# Fedora guidelines say Group tag optional, but OBS for SuSE complains if not present 
Group: Applications/System

# Fedora guidelines say BuildRoot ignored
BuildRoot: %{_tmppath}/%{name}-%{version}-build


# if description comes before tags, it gobbles them up into 
# the description, or at least rpmlint thinks it does
%description 
Query and change monitor settings

ddcutil communicates with monitors implementing MCCS (Monitor Control Command
Set), using either the DDC/CI protocol on the I2C bus or as a Human Interface
Device on USB.

A particular use case for ddcutil is as part of color profile management.
Monitor calibration is relative to the monitor color settings currently in
effect, e.g. red gain.  ddcutil allows color related settings to be saved at
the time a monitor is calibrated, and then restored when the calibration is
applied.


%package -n libddcutil0
Summary: Shared library to query and update monitor settings 
Group: System Environment/Libraries

%description -n libddcutil0 
Shared library version of ddcutil, exposing a C API.  

ddcutil communicates with monitors implementing MCCS (Monitor Control Command
Set), using either the DDC/CI protocol on the I2C bus or as a Human Interface
Device on USB.


%package -n libddcutil-devel
Summary: Development files for libddcutil
Group: Development/Libraries
Requires: libddcutil0 >= %{version}

%description -n libddcutil-devel
Header files, pkgconfig control file, static libraries, 
maybe some doc for libddcutil.


%prep
%setup 
# %%setup -q
rpm --version
rpmbuild --version

%build
%if %{build_libs} == 1
%{echo: =================================> building libraries, }
#%%configure -enable-lib=yes
%define conf_lib_parm yes
%else
%{echo: =================================> NOT building libraries, }
#%%configure -enable-lib=no
%define conf_lib_parm no
%endif

%define conf_usb_parm yes
%define conf_drm_parm no
%if %{is_obs_build}
   %if 0%{?suse_version}
      %if 0%{?suse_version} <= 1310
        %define conf_usb_parm no
      %endif
      # suse_version == 1315 if Leap, check sle_version for Leap version, sle_version == 120200 for Leap 42.2
      # suse_version == 1330 if Tumbleweed
      %if 0%{?suse_version} == 1315
         %{echo: conf_drm_parm: Leap, }
         %if 0%{?sle_version} >= 120200
            %{echo: conf_drm_parm: Leap ge 42.1, }
            %define conf_drm_parm yes
	 %endif
      %endif
      %if 0%{?suse_version} == 1330
         %{echo: conf_drm_parm: Tumbleweed, }
         %define conf_drm_parm yes
      %endif
   %endif
   %if 0%{?fedora_version} >= 24
      %define conf_drm_parm yes 
   %endif
%else
   %define conf_drm_parm yes 
%endif


%{echo:conf_usb_parm  is %{?conf_usb_parm}, }
%{echo:conf_drm_parm  is %{?conf_drm_parm}, }
         

%configure --enable-lib=%{conf_lib_parm} --enable-drm=%{conf_drm_parm} --enable-usb=%{conf_usb_parm}
make V=1

%check
%{echo: =================================> Executing make check, }
make check

%install
%{echo: =================================> Executing make install, }
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_datadir}/doc/%{name}/html

# Fedora guidelines: %%clean section not required
%clean
rm -rf %{buildroot}

%files
%defattr(664,root,root)
# %%doc %%{_datadir}/doc/%%{name}/AUTHORS
# %%doc %%{_datadir}/doc/%%{name}/ChangeLog
# %%doc %%{_datadir}/doc/%%{name}/COPYING
# %%doc %%{_datadir}/doc/%%{name}/INSTALL
# %%doc %%{_datadir}/doc/%%{name}/NEWS 
# %%doc %%{_datadir}/doc/%%{name}/README
# would copy entire directory:
# %%{_datadir}/%{name}/
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/data
%{_datadir}/%{name}/data/*rules
%{_datadir}/%{name}/data/90-nvidia-i2c.conf
%{_mandir}/man1/ddcutil.1*
%attr(755,root,root)%{_bindir}/ddcutil


%files -n libddcutil0
%if %{build_libs} == 1
%{echo: ============================> files: building libraries, }
%defattr(-,root,root)
%{_libdir}/libddcutil.so.*
%else
%{echo: ============================> files: NOT building libraries, }
%endif


%files -n libddcutil-devel
%defattr(-,root,root)
%{_libdir}/libddcutil.a
%{_libdir}/libddcutil.la
%{_includedir}/ddcutil_types.h
%{_includedir}/ddcutil_c_api.h
%{_libdir}/pkgconfig/ddcutil.pc
%{_libdir}/libddcutil.so
# Fails on SuSE, lack permissions to write to Modules
# %%{_datadir}/cmake/Modules/FindDDCUtil.cmake
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data/
%{_datadir}/%{name}/data/FindDDCUtil.cmake


# %%doc -n ddcutil
# %%doc -n libddcutil-0
# %%doc -n libddcutil-devel

%post   -n libddcutil0 -p /sbin/ldconfig
%postun -n libddcutil0 -p /sbin/ldconfig


%changelog

* Mon May 01 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.0-1

  Release 0.8.0

* Sun Mar 05 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.7.3-1

  Release 0.7.3

* Mon Jan 02 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.7.0-1

- Release 0.7.0

- Added packages libddcutil0 and libddcutil-devel

