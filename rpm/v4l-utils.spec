Name:           v4l-utils
Version:        1.26.1
Release:        1%{?dist}
Summary:        Utilities for video4linux and DVB devices
# libdvbv5, dvbv5 utils, ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/

Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2

BuildRequires:  alsa-lib-devel
BuildRequires:  gettext
BuildRequires:  kernel-headers
BuildRequires:  libjpeg-devel
BuildRequires:  qt5-qtcore-devel
BuildRequires:  pkgconfig(systemd)
BuildRequires:  libtool
BuildRequires:  meson >= 0.56
BuildRequires:  qt5-qtwidgets-devel

# BPF decoder dependencies
%define with_bpf 0

%if %{with_bpf}
BuildRequires:  elfutils-libelf-devel clang
%endif

# For /lib/udev/rules.d ownership
Requires:       udev
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
# decode_tm6000 is GPLv2 only
License:        GPLv2+ and GPLv2
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 / DVB driver authors: decode_tm6000, v4l2-compliance and
v4l2-dbg.

%package -n     libv4l
Summary:        Collection of video4linux support libraries 
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.


%package -n     libdvbv5
Summary:        Libraries to control, scan and zap on Digital TV channels
License:        GPLv2

%description -n libdvbv5
Libraries to control, scan and zap on Digital TV channels

%package -n     libv4l-devel
Summary:        Development files for libv4l
License:        LGPLv2+
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.


%package -n     libdvbv5-devel
Summary:        Development files for libdvbv5
License:        GPLv2
Requires:       libdvbv5%{?_isa} = %{version}-%{release}

%description -n libdvbv5-devel
The libdvbv5-devel package contains libraries and header
files for developing applications that use libdvbv5.

%package -n libdvbv5-gconv
Summary:        Gconv files with the charsets For Digital TV.
License:        LGPL-2.1-or-later

%description -n libdvbv5-gconv
Some digital TV standards define their own charsets. Add library
support for them: EN 300 468 and ARIB STD-B24


%prep
%autosetup -p1

%build
cd v4l-utils
%meson -Dbpf=disabled -Ddoxygen-doc=false -Ddoxygen-man=false -Ddoxygen-html=false -Dqv4l2=enabled \
        -Dqvidcap=disabled -Dv4l2-tracer=disabled

%meson_build


%install
cd v4l-utils
%{!?_udevrulesdir: %global _udevrulesdir /lib/udev/rules.d}
%meson_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_libdir}/{v4l1compat.so,v4l2convert.so}
%find_lang %{name}

%post -n libv4l -p /sbin/ldconfig
%post -n libdvbv5 -p /sbin/ldconfig
%postun -n libv4l -p /sbin/ldconfig
%postun -n libdvbv5 -p /sbin/ldconfig

%files -f v4l-utils/%{name}.lang
%doc v4l-utils/README.md
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
%{_udevrulesdir}/70-infrared.rules
%{_udevrulesdir}/../rc_keymaps/*
%{_bindir}/cx18-ctl
%{_bindir}/cec*
%{_bindir}/dvb*
%{_bindir}/ir-ctl
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/media-ctl
%{_bindir}/rds-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%exclude %{_mandir}/man1/v4l2-compliance.1*

%files devel-tools
%doc v4l-utils/README.md
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_sbindir}/v4l2-dbg
%{_mandir}/man1/v4l2-compliance.1*
%{_bindir}/qv4l2
%{_datadir}/icons/hicolor/*/apps/qv4l2.*

%files -n libv4l
%doc v4l-utils/ChangeLog v4l-utils/README.libv4l v4l-utils/TODO
%license v4l-utils/COPYING.libv4l v4l-utils/COPYING
%{_libdir}/libv4l
%{_libdir}/libv4l*.so.*

%files -n libv4l-devel
%doc v4l-utils/README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc

%files -n libdvbv5
%doc v4l-utils/ChangeLog v4l-utils/lib/libdvbv5/README
%license v4l-utils/COPYING
%{_libdir}/libdvbv5*.so.*

%files -n libdvbv5-devel
%{_includedir}/libdvbv5/*.h
%{_libdir}/libdvbv5*.so
%{_libdir}/pkgconfig/libdvbv5*.pc

%files -n libdvbv5-gconv
%{_libdir}/gconv/*.so
%{_libdir}/gconv/gconv-modules.d/libdvbv5.conf

%changelog
* Sun Sep 8 2019 Dylan Van Assche <dylan.van.assche@protonmail.com> 1.6.1-1 
- Initial mer-core package

