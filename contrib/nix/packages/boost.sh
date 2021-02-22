source "$stdenv/setup"
set -efuo pipefail

tar -xf "$src"
cd "$(ls | grep -v 'env-vars')"

: ./depends Preprocessing
for patch in $patches
do
  echo "Applying patch: $patch"
  patch -p2 < "$patch"
done

: ./depends Configuring
./bootstrap.sh --without-icu --with-libraries="$boostlibs"

# FIXME: port this patch from ./depends:
#sed -i -e "s|using gcc ;|using $(boost_toolset_$(host_os)) : : $($(package)_cxx) : <cxxflags>\"$($(package)_cxxflags) $($(package)_cppflags)\" <linkflags>\"$($(package)_ldflags)\" <archiver>\"$(boost_archiver_$(host_os))\" <striper>\"$(host_STRIP)\"  <ranlib>\"$(host_RANLIB)\" <rc>\"$(host_WINDRES)\" : ;|" project-config.jam

: ./depends Building
./b2 -d2 -j2 -d1 --prefix="$out" $configureFlags cxxflags="$cxxFlags" stage

: ./depends Staging
./b2 -d0 -j4 --prefix="$out" $configureFlags install