#!/bin/bash

SETS=$1

BUILD="asan"
COMBO="$BUILD-$SETS"

cp $BUILD.bldconf $COMBO.bldconf

if [ "$SETS" == "profile" ]; then
  EXTRA_CFLAGS="-fno-inline -pg"
  EXTRA_CXXFLAGS="-fno-inline -pg"
  EXTRA_LDFLAGS="-fno-inline -pg"
fi

echo "export LDFLAGS=\"$EXTRA_LDFLAGS -fsanitize=address -flto -fuse-ld=gold -L\${CC_HOME}/lib64 -L\${CC_HOME}/lib\"" | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf

echo "export CXXFLAGS=\"-O3 -g -stdlib=libstdc++ $EXTRA_CXXFLAGS -fsanitize=address -funroll-loops -fpermissive -fno-exceptions -flto \${PORTABILITY_FLAGS}\"" | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf

echo "export CFLAGS=\" -O3 -g $EXTRA_CFLAGS -fsanitize=address -funroll-loops -fprefetch-loop-arrays -flto \${PORTABILITY_FLAGS}\"" | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf

echo '#!/bin/bash' | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf

mv $COMBO.bldconf $WKS/config/$COMBO.bldconf

cp $PARMACS/parsec/gcc-pthreads.bldconf $PARMACS/parsec/$COMBO.bldconf

export ASAN_OPTIONS=detect_leaks=0,detect_odr_violation=0
