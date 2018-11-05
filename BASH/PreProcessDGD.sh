#  Bash-Skript zum Sammeln der Länderinformationen Stand 2017- Feb 2018
#  Denis Arnold

if [ ! $# == 2 ]; then
        echo "Usage:"
        echo "PreProcessDGD.sh metadataroot newcorpusdatafolder"
        echo "metadataroot is the folder in which the metadata is stored. Usually dgd2data/metadata"
        echo "newcorpusdata is the name of an existing folder where the output should be stored"
        exit
fi

#set -ex

for j in $1/corpora/extern/*;
        do corp=$(echo $j | sed "s|$1||g" | sed "s|"\/corpora\/extern\/"||g" |  sed "s|"-*_extern\.xml"||g");
        corpora=$(echo $j | sed "s|$1||g" | sed "s|"\/corpora\/extern\/"||g" );
        for i in $1/events/extern/$corp/*; 
                do xmllint --format $i | grep -E "<Land" | sed s/"<Land Kürzel=\".*\">"//g  | sed s/"<\/Land>"//g | sed s/"\ \ "//g >> LOG; 
        done; 
        fun="$(cat LOG | sort -u | tr -d "\r" | paste -sd ";")" 
        xmllint --format $j | sed "s|<Länder_Regionen_Orte>.*</Länder_Regionen_Orte>|<Länder_Regionen_Orte>$fun</Länder_Regionen_Orte>|g" > $2/$corpora
        rm LOG;
done;

