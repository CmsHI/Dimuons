# for the list of used tags please see:
# https://twiki.cern.ch/twiki/bin/view/CMS/Onia2MuMuSamples

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# set up process
process = cms.Process("Onia2MuMuPAT")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

# setup any defaults you want
options.outputFile = 'onia2MuMuPAT.root'
options.inputFiles = '/store/caf/user/tdahms/Data2013/pPb/ExpressSkims/Run_210498/pAMuonDimuon.root'
options.maxEvents = -1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = 'GR_E_V33::All'
#process.GlobalTag.globaltag = 'GR_P_V43D::All'

# Common offline event selection
process.load("HeavyIonsAnalysis.Configuration.collisionEventSelection_cff")

# Centrality for pPb
process.load('RecoHI.HiCentralityAlgos.HiCentrality_cfi')

# HLT dimuon trigger
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltOniaHI = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltOniaHI.HLTPaths = ["HLT_PAL1DoubleMuOpen_v*",
                              "HLT_PAL1DoubleMu0_HighQ_v*",
                              "HLT_PAL2DoubleMu3_v*",
                              "HLT_PAMu3_v*",
                              "HLT_PAMu7_v*",
                              "HLT_PAMu12_v*",
                              "HLT_PAPixelTrackMultiplicity100_L2DoubleMu3_v*"
                              ]
process.hltOniaHI.throw = False
process.hltOniaHI.andOr = True
process.hltOniaHI.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")


from HiSkim.HiOnia2MuMu.onia2MuMuPAT_cff import *
onia2MuMuPAT(process, GlobalTag=process.GlobalTag.globaltag, MC=False, HLT="HLT", Filter=True)

#process.onia2MuMuPatTrkTrk.addMuonlessPrimaryVertex = False
#process.onia2MuMuPatTrkTrk.resolvePileUpAmbiguity = False

process.source.fileNames = cms.untracked.vstring(
    options.inputFiles
    )

# filter on lumisections
#from HiSkim.HiOnia2MuMu.goodLumiSectionListHI_cfi import *
#process.source.lumisToProcess = goodLumisToProcess

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.outOnia2MuMu.fileName = cms.untracked.string( options.outputFile )
process.pACentrality_step = cms.Path(process.hltOniaHI*process.PAcollisionEventSelection*process.pACentrality)

process.e = cms.EndPath(process.outOnia2MuMu)

process.schedule = cms.Schedule(process.pACentrality_step,
                                process.Onia2MuMuPAT,process.e)


