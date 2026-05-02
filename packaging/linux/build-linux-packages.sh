#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?version is required}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="${ROOT_DIR}/release/linux"
PKG_DIR="${ROOT_DIR}/release/packages"
APP_NAME="safelink"
DISPLAY_NAME="SafeLink"

rm -rf "${BUILD_DIR}" "${PKG_DIR}"
mkdir -p "${BUILD_DIR}" "${PKG_DIR}"

python -m pip install --upgrade pip
python -m pip install -r "${ROOT_DIR}/requirements.txt" pyinstaller
pyinstaller --clean --noconfirm "${ROOT_DIR}/SafeLink.spec"

install_common_files() {
  local target_root="$1"

  install -Dm755 "${ROOT_DIR}/dist/SafeLink" "${target_root}/opt/safelink/SafeLink"
  install -Dm644 "${ROOT_DIR}/assets/safelink-logo.png" "${target_root}/usr/share/icons/hicolor/512x512/apps/safelink.png"
  install -Dm644 "${ROOT_DIR}/packaging/linux/safelink.desktop" "${target_root}/usr/share/applications/safelink.desktop"
}

build_deb() {
  local root="${BUILD_DIR}/deb-root"
  local debian="${root}/DEBIAN"

  install_common_files "${root}"
  mkdir -p "${debian}"

  cat > "${debian}/control" <<CONTROL
Package: ${APP_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: SafeLink
Depends: libc6, libx11-6, tk
Description: SafeLink URL reputation checker
 SafeLink verifies URLs with the VirusTotal API using a desktop interface.
CONTROL

  dpkg-deb --build --root-owner-group "${root}" "${PKG_DIR}/${APP_NAME}_${VERSION}_amd64.deb"
  cp "${PKG_DIR}/${APP_NAME}_${VERSION}_amd64.deb" "${PKG_DIR}/${APP_NAME}_amd64.deb"
}

build_rpm() {
  local topdir="${BUILD_DIR}/rpmbuild"
  local root="${BUILD_DIR}/rpm-root"
  local tar_dir="${BUILD_DIR}/${APP_NAME}-${VERSION}"
  local spec="${topdir}/SPECS/${APP_NAME}.spec"

  install_common_files "${root}"
  mkdir -p "${topdir}/"{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS,TMP} "${tar_dir}"
  cp -a "${root}/." "${tar_dir}/"
  tar -C "${BUILD_DIR}" -czf "${topdir}/SOURCES/${APP_NAME}-${VERSION}.tar.gz" "${APP_NAME}-${VERSION}"

  cat > "${spec}" <<SPEC
%global debug_package %{nil}

Name: ${APP_NAME}
Version: ${VERSION}
Release: 1%{?dist}
Summary: SafeLink URL reputation checker
License: MIT
Source0: %{name}-%{version}.tar.gz
BuildArch: x86_64
Requires: glibc
Requires: libX11
Requires: tk

%description
SafeLink verifies URLs with the VirusTotal API using a desktop interface.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}
cp -a opt usr %{buildroot}/

%files
/opt/safelink/SafeLink
/usr/share/applications/safelink.desktop
/usr/share/icons/hicolor/512x512/apps/safelink.png

%changelog
* Sat May 02 2026 SafeLink <noreply@example.com> - ${VERSION}-1
- Build SafeLink release package.
SPEC

  rpmbuild --define "_topdir ${topdir}" --define "_tmppath ${topdir}/TMP" -bb "${spec}"
  local rpm_file
  rpm_file="$(find "${topdir}/RPMS/x86_64" -maxdepth 1 -type f -name "${APP_NAME}-${VERSION}-1*.x86_64.rpm" | sort | head -n 1)"
  if [[ -z "${rpm_file}" ]]; then
    echo "No RPM package was produced in ${topdir}/RPMS/x86_64" >&2
    exit 1
  fi
  cp "${rpm_file}" "${PKG_DIR}/${APP_NAME}-${VERSION}-fedora-x86_64.rpm"
  cp "${PKG_DIR}/${APP_NAME}-${VERSION}-fedora-x86_64.rpm" "${PKG_DIR}/${APP_NAME}-fedora-x86_64.rpm"
}

build_deb
build_rpm
