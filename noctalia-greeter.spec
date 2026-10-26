Name:           noctalia-greeter
Version:        1.7.0
Release:        1
Summary:        A greetd greeter, tightly coupled with Noctalia.
License:        MIT
URL:            https://github.com/noctalia-dev/noctalia-greeter
Source0:        https://github.com/noctalia-dev/noctalia-greeter/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wlroots-0.20)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(nlohmann_json)
BuildRequires:  pkgconfig(stb)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libxml-2.0)

Requires: greetd
Requires: dbus-daemon
Requires: accountsservice

%description
Noctalia Greeter is the screen you see before your desktop session starts. It lets you pick a user, enter your password, choose a Wayland session, and pick a color scheme - with the same visual language as Noctalia. A configurable clock uses Noctalia-compatible time/date formats, separate time and date font sizes, and the active greeter palette.

Long session and color scheme menus fit within the screen and show a scrollbar. Use the mouse wheel, drag the scrollbar, or navigate with the arrow keys; see keyboard and cursor controls.

It is built for greetd: greetd launches noctalia-greeter-session, which starts the bundled wlroots compositor and runs the greeter inside that session.

Pair it with Noctalia v5 if you want wallpaper and palette synced from the shell settings (optional).

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

# The setup library is sourced by other shell scripts.
chmod 0644 %{buildroot}%{_datadir}/noctalia-greeter/greetd_setup_lib.sh

# Replace env-based shell interpreters with absolute paths.
# Preserve Bash for scripts that use Bash-specific syntax.
for script in 
    %{buildroot}%{_bindir}/noctalia-greeter-session 
    %{buildroot}%{_bindir}/noctalia-greeter-print-greetd-config 
    %{buildroot}%{_bindir}/noctalia-greeter-xsession 
    %{buildroot}%{_datadir}/noctalia-greeter/*.sh
do
    [ -f "$script" ] || continue

    case "$(head -n1 "$script")" in
        '#!/usr/bin/env bash')
            sed -i '1c\#!/usr/bin/bash' "$script"
            ;;
        '#!/usr/bin/env sh')
            sed -i '1c\#!/usr/bin/sh' "$script"
            ;;
    esac
done

%files
%license LICENSE
%doc README.md
%{_bindir}/noctalia-greeter
%{_bindir}/noctalia-greeter-xsession
%{_bindir}/noctalia-greeter-compositor
%{_bindir}/noctalia-greeter-session
%{_bindir}/noctalia-greeter-apply-appearance
%{_bindir}/noctalia-greeter-print-greetd-config
%{_datadir}/noctalia-greeter
%{_datadir}/polkit-1/actions/org.noctalia.greeter.apply-appearance.policy
%{_prefix}/lib/tmpfiles.d/noctalia-greeter.conf
