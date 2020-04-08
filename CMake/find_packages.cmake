find_package(X11 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(VTK)
find_package(GTK2)
find_package(CGAL REQUIRED COMPONENTS Core)
find_package(GNUGTS REQUIRED)
find_package(CImg REQUIRED)
find_package(MySQL)
find_package(GLIB2)
find_package(PythonInterp)
find_package(PythonLibs REQUIRED)
find_package(Boost 1.45.0)
if(Boost_FOUND)
  INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
  SET(Boost_USE_STATIC_LIBS OFF)
  SET(Boost_USE_MULTITHREADED ON)
#  SET(Boost_USE_STATIC_RUNTIME OFF)
  if (PYTHON_VERSION_MAJOR EQUAL 3)
     find_package(Boost COMPONENTS python${PYTHON_VERSION_SUFFIX})
     find_package(PythonInterp 3)
     find_package(PythonLibs 3 REQUIRED)
  else()
     find_package(Boost COMPONENTS python)
     find_package(PythonInterp)
     find_package(PythonLibs REQUIRED)
  endif()
  set(XC_UTILS_BOOST_PYTHON_LIBRARIES ${Boost_LIBRARIES})
  find_package(Boost COMPONENTS system regex filesystem thread math_c99 math_c99f math_c99l math_tr1 math_tr1f math_tr1l REQUIRED)
elseif(NOT Boost_FOUND)
  MESSAGE(FATAL_ERROR "Unable to find correct Boost version. Did you set BOOST_ROOT?")
endif()
#MESSAGE(STATUS "boost libraries: " ${Boost_LIBRARIES})
find_package(F2C REQUIRED)
find_package(Plot REQUIRED)
find_package(Gnuplot REQUIRED)
find_package(MPFR)
find_package(GMP)
find_package(SQLITE3 REQUIRED)
find_package(MPI)
find_package(Arpack REQUIRED)
find_package(ArpackPP REQUIRED)
find_package(Petsc)
find_package(LAPACK REQUIRED)
find_package(BLAS REQUIRED)
find_package(SuperLU REQUIRED)
find_package(BerkeleyDB REQUIRED)
find_package(METIS REQUIRED)
find_package(TCL REQUIRED)
find_package(ORACLE)
find_package(OpenMP REQUIRED)
