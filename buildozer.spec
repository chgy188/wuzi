[app]

# (str) Title of your application
title = 五子棋

# (str) Package name
package.name = gomoku

# (str) Package domain (needed for android/ios packaging)
package.domain = org.myapp

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy,numpy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT_TO_PY2

#
# OSX Specific
#

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, grey, lightgray, darkgray, cyan, magenta,
# yellow, lightred, lightblue, lightgreen, lightgrey, lightmagenta, lightyellow,
# darkred, darkblue, darkgreen, darkgrey, darkcyan, darkmagenta, darkyellow
#presplash.color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK version to use
#android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir-external storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automated testing environments.
# This can be dangerous to use
#android.accept_sdk_license = False

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Android .aars libraries to add (unlike Java jars, .aars are native libraries)
#android.add_aars =

# (list) Gradle dependencies to add (currently needs Java to be installed)
#android.gradle_dependencies =

# (list) Java classes to add as parts of the Java app
#android.add_jars =

# (list) Java files to add as parts of the Java app
#android.add_sources =

# (list) Android Java libs to add (will be compiled by the default javac compiler)
#android.add_libs =

# (list) Android AAR archives to add (will be extracted by Gradle)
#android.add_aars =

# (list) Put Java files in this folder. See the java folder inclusion example
#android.java_src_folder =

# (list) put Python files in this folder. See the python folder inclusion example
#android.python_src_folder =

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) Ouyang Console executable. This presently works if pygame is used as a
# root widget and you want to redirect the console output to the Ouyang console.
#ouyang.console.executable = /data/data/net.handsome.ouyang/files/bin/ouyang

# (str) Android arch to use for compilation
android.archs = arm64-v8a,armeabi-v7a

# (int) Android API level to use for compilation
#android.api = 21

# (str) NDK version to use
#android.ndk = 19b

# (int) Minimum Android API level to compile against
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 21

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) python-for-android clone directory (if empty, it will be automatically cloned from github)
#android.p4a_dir =

# (str) Python-for-android fork to use (defaults to upstream kivy)
#android.p4a_fork =

# (str) python-for-android specific branch to use, defaults to master
#android.p4a_branch =

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a_branch
#android.p4a_commit =

# (str) URL to python-for-android git repository (defaults to upstream kivy)
#android.p4a_repo =

# (list) python-for-android recipe to use
#android.recipe = python3

# (str) Bootstrap to use (default is sdl2)
#android.bootstrap = sdl2

# (int) Number of parallel builds during build
#android.parallel_jobs = 1

# (int) Android NDK API level to use (default is 21)
#android.ndk_api = 21

# (bool) If True, then use the Python 3 toolchain (defaults to True)
#android.use_python3 = True

# (bool) If True, then use Python 2.7 toolchain (defaults to False)
#android.use_python2 = False

# (list) List of library .a files to add (can be file glob)
#android.add_libs_armeabi =
#android.add_libs_armeabi_v7a =
#android.add_libs_arm64_v8a =
#android.add_libs_x86 =
#android.add_libs_mips =

# (bool) Whether to copy your application's AndroidManifest.xml
#android.copy_manifest = False

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (list) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Android logcat only on logcat stream. True if you want to disable logging on standard output.
android.logcat_log_only = True

# (str) The Android arch to build for, choices: arm64-v8a, armeabi-v7a
#android.arch = arm64-v8a

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for cloning
#p4a.url =

# (str) python-for-android directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) python-for-android branch to use
#p4a.branch = master

# (str) python-for-android commit to use (must be on p4a.branch)
#p4a.commit =

# (str) python-for-android git repository URL (defaults to upstream kivy)
#p4a.repo =

# (str) python-for-android recipe to use
#p4a.recipe = python3

# (int) Minimum Android API level to compile against (default is 21)
#p4a.min_api = 21

# (int) Android NDK API level to use (default is 21)
#p4a.ndk_api = 21

# (bool) If True, then use the Python 3 toolchain (defaults to True)
#p4a.use_python3 = True

# (bool) If True, then use Python 2.7 toolchain (defaults to False)
#p4a.use_python2 = False

# (str) Name of the directory in which the Python for android distribution will be stored
#p4a.dist_name =

# (str) Bootstrap to use (default is sdl2)
#p4a.bootstrap = sdl2

#
# iOS specific
#

#
# Mac OS X specific
#

#
# Windows specific
#

# (str) WMSIX icon (if using WMSIX)
#wmsix.icon = data/icon.png

# (list) WMSIX architectures to build (if using WMSIX)
#wmsix.archs = arm64

# (str) WMSIX publisher (if using WMSIX)
#wmsix.publisher = org.kivy

# (list) WMSIX capabilities (if using WMSIX)
#wmsix.capabilities = internetClient,location,microphone,webcam

# (bool) WMSIX install on startup (if using WMSIX)
#wmsix.install_on_startup = True

# (list) WMSIX file associations (if using WMSIX)
#wmsix.file_associations =

# (list) WMSIX URI schemes (if using WMSIX)
#wmsix.uri_schemes =

#
# Metadata
#

# (str) Application author
author = Your Name

# (str) Application author email
author_email = your.email@example.com

# (str) Application description
description = 五子棋游戏，支持人机对战