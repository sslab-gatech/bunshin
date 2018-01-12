#!/bin/bash

SAN=$1

BUILD="vsplit"
COMBO="$BUILD-$SAN"

USAGE="Usage: $0 <sanitizer> <original | trace | bft> <nvar> <spec name>"

cp $BUILD.bldconf $COMBO.bldconf 

echo "export LDFLAGS=\"-flto -fsanitize=$SAN -fuse-ld=gold -L\${CC_HOME}/lib64 -L\${CC_HOME}/lib\"" | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf 

echo "export CXXFLAGS=\"-O3 -g -stdlib=libstdc++ -funroll-loops -fpermissive -fno-exceptions -flto -fsanitize=$SAN \${PORTABILITY_FLAGS}\"" | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf 

echo "export CFLAGS=\" -O3 -g -flto -funroll-loops -fsanitize=$SAN -fprefetch-loop-arrays \${PORTABILITY_FLAGS}\"" | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf 
echo '#!/bin/bash' | cat - $COMBO.bldconf > tmp && mv tmp $COMBO.bldconf 

mv $COMBO.bldconf $WKS/config/$COMBO.bldconf

cp $PARMACS/parsec/gcc-pthreads.bldconf $PARMACS/parsec/$COMBO.bldconf
