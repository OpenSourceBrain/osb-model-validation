#!/bin/bash

################################################################################
#
#  This is a helper script to pull all core* OSB projects from GitHub to 
#  facilitate testing, etc.
#
#  *projects which are known to contain valid NeuroML/PyNN & have passing OMV 
#   tests
#
################################################################################

pull=false

function gitss () {
    tput setaf 5
    git rev-parse --abbrev-ref HEAD
    tput setaf 3
    git status -s
    tput setaf 2
    git fetch --dry-run
    git stash list
    tput setaf 9
}

function gitpp () {
    tput setaf 2
    git pull -p
    tput setaf 9
}


pull=true
echo "Pulling latest core projects..."

startDir=$(pwd)

prefix='git@github.com:'

if [ -z "$USE_SSH_FOR_GITHUB" ]; then
    echo
    echo "If you use SSH to access GitHub, set the environment variable USE_SSH_FOR_GITHUB to 1"
    echo "This will clone GitHub repos using SSH. Using HTTPS instead"
    echo
    prefix='https://github.com/'
fi

prefixBB='https://bitbucket.org/'


standardGHProject()
{
    echo
    echo "-----  Checking:" $2/$1
    tput setaf 1

    if [ ! -d $2 ]; then
        parent=$2
        parent=${parent%/*}
        if [ ! -d $parent ]; then
            mkdir $parent
            echo "Making new directory: " $parent
            
        fi
        mkdir $2
        echo "Making new directory: " $2
        
    fi
    tgtDir=$startDir/$2/$1
    

    if [ ! -d $tgtDir ]; then
        echo "Cloning to: "$tgtDir
        if [ $# == 3 ]; then
            echo "Using repo: "$prefix$3/$1.git
            git clone $prefix$3/$1.git $tgtDir
        else
            osbOrg='OpenSourceBrain'
            echo "Using repo: "$prefix$osbOrg/$1.git
            git clone $prefix$osbOrg/$1.git $tgtDir
        fi
    fi

    cd $tgtDir
    if $pull; then
        gitpp
    else
        gitss
    fi

    cd $startDir
}


standardBBProject()
{
    echo
    echo "-----  Checking:" $2/$1
    tput setaf 1

    if [ ! -d $2 ]; then
        parent=$2
        parent=${parent%/*}
        if [ ! -d $parent ]; then
            mkdir $parent
            echo "Making new directory: " $parent
        fi
        mkdir $2
        echo "Making new directory: " $2

    fi
    tgtDir=$startDir/$2/$1

    if [ ! -d $tgtDir ]; then
        echo "Cloning to: "$tgtDir
        if [ $# == 3 ]; then
            echo "Using repo: "$prefixBB$3/$1
            hg clone $prefixBB$3/$1 $tgtDir
        else
            osbOrg='OpenSourceBrain'
            echo "Using repo: "$prefixBB$osbOrg/$1
            hg clone $prefixBB$osbOrg/$1 $tgtDir
        fi
    fi

    cd $tgtDir
    if $pull; then
        hgpp
    else
        hgss
    fi

    cd $startDir
}



standardGHProject 'BlueBrainProjectShowcase' 'coreprojects'
standardGHProject 'AllenInstituteNeuroML' 'coreprojects'
standardGHProject 'PotjansDiesmann2014' 'coreprojects'
standardGHProject 'L5bPyrCellHayEtAl2011' 'coreprojects'
standardGHProject 'SmithEtAl2013-L23DendriticSpikes'  'coreprojects'
standardGHProject 'IzhikevichModel' 'coreprojects'
standardGHProject 'Thalamocortical' 'coreprojects'
##standardGHProject 'VERTEXShowcase' 'coreprojects'
standardGHProject 'Brunel2000' 'coreprojects'
standardGHProject 'PospischilEtAl2008' 'coreprojects'
standardGHProject 'M1NetworkModel' 'coreprojects'
standardGHProject 'SadehEtAl2017-InhibitionStabilizedNetworks' 'coreprojects'


standardGHProject 'SolinasEtAl-GolgiCell' 'coreprojects'
standardGHProject 'GranCellLayer' 'coreprojects'
standardGHProject 'VervaekeEtAl-GolgiCellNetwork' 'coreprojects'
standardGHProject 'MF-GC-network-backprop-public' 'coreprojects' 'SilverLabUCL'

standardGHProject 'CA1PyramidalCell' 'coreprojects'
standardGHProject 'FergusonEtAl2013-PVFastFiringCell' 'coreprojects'
standardGHProject 'PinskyRinzelModel' 'coreprojects'
standardGHProject 'WangBuzsaki1996' 'coreprojects'

standardGHProject 'ca1' 'coreprojects' 'mbezaire'
cd coreprojects/ca1
git checkout development
git pull
cd -

standardGHProject 'MiglioreEtAl14_OlfactoryBulb3D' 'coreprojects'

standardGHProject 'FitzHugh-Nagumo' 'coreprojects'
standardGHProject 'hodgkin_huxley_tutorial' 'coreprojects' 'openworm'
standardGHProject 'muscle_model' 'coreprojects' 'openworm'
standardGHProject 'PyloricNetwork' 'coreprojects'

standardGHProject 'NeuroMorpho' 'coreprojects'
standardGHProject 'MouseLightShowcase' 'coreprojects'

cd $startDir



