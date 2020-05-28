#include "wsjcpp_package_manager_distribution_file.h"
#include <wsjcpp_core.h>

// ---------------------------------------------------------------------
// WsjcppPackageManagerDistributionFile

WsjcppPackageManagerDistributionFile::WsjcppPackageManagerDistributionFile() {
    TAG = "WsjcppPackageManagerDistributionFile";
}

// ---------------------------------------------------------------------

bool WsjcppPackageManagerDistributionFile::fromYAML(WsjcppYamlItem *pYamlDistributionFile, bool bHolded) {
    m_bHolded = bHolded;
    m_pYamlDistributionFile = pYamlDistributionFile;
    if (!m_pYamlDistributionFile->hasElement("source-file")) {
        WsjcppLog::err(TAG, "Missing required field 'source-file' in " + m_pYamlDistributionFile->getForLogFormat());
        return false; 
    } else {
        m_sSourceFile = m_pYamlDistributionFile->getElement("source-file")->getValue();
    }

    if (!m_pYamlDistributionFile->hasElement("target-file")) {
        WsjcppLog::err(TAG, "Missing required field 'target-file' in " + m_pYamlDistributionFile->getForLogFormat());
        return false; 
    } else {
        m_sTargetFile = m_pYamlDistributionFile->getElement("target-file")->getValue();
    }

    if (m_pYamlDistributionFile->hasElement("sha1")) {
        m_sSha1 = m_pYamlDistributionFile->getElement("sha1")->getValue();
    }

    if (m_bHolded) {
        if (!m_pYamlDistributionFile->hasElement("sha1")) {
            m_pYamlDistributionFile->setElementValue("sha1", false, "", true);
            // TODO WsjcppLog::err(TAG, "Missing required field 'sha1' in " + m_pYamlDistributionFile->getForLogFormat());
            // return false; 
        } else {
            m_sSha1 = m_pYamlDistributionFile->getElement("sha1")->getValue();
        }
    }

    if (!m_pYamlDistributionFile->hasElement("type")) {
        WsjcppLog::err(TAG, "Missing required field 'type' in " + m_pYamlDistributionFile->getForLogFormat());
        return false; 
    } else {
        m_sType = m_pYamlDistributionFile->getElement("type")->getValue();
    }

    // TODO check possible formats

    return true;
}

// ---------------------------------------------------------------------

WsjcppYamlItem *WsjcppPackageManagerDistributionFile::toYAML() {
    m_pYamlDistributionFile->getElement("source-file")->setValue(m_sSourceFile, true);
    m_pYamlDistributionFile->getElement("target-file")->setValue(m_sTargetFile, true);
    m_pYamlDistributionFile->getElement("sha1")->setValue(m_sSha1, true);
    m_pYamlDistributionFile->getElement("type")->setValue(m_sType, true);
    return m_pYamlDistributionFile;
}

// ---------------------------------------------------------------------

std::string WsjcppPackageManagerDistributionFile::getSourceFile() {
    return m_sSourceFile;
}

// ---------------------------------------------------------------------

std::string WsjcppPackageManagerDistributionFile::getTargetFile() {
    return m_sTargetFile;
}

// ---------------------------------------------------------------------

std::string WsjcppPackageManagerDistributionFile::getSha1() {
    return m_sSha1;
}

// ---------------------------------------------------------------------

std::string WsjcppPackageManagerDistributionFile::getType() {
    return m_sType;
}

// ---------------------------------------------------------------------

void WsjcppPackageManagerDistributionFile::setSourceFile(const std::string &sSourceFile) {
    m_sSourceFile = sSourceFile;
}

// ---------------------------------------------------------------------

void WsjcppPackageManagerDistributionFile::setTargetFile(const std::string &sTargetFile) {
    m_sTargetFile = sTargetFile;
}

// ---------------------------------------------------------------------

void WsjcppPackageManagerDistributionFile::setSha1(const std::string &sSha1) {
    m_sSha1 = sSha1;
}

// ---------------------------------------------------------------------

void WsjcppPackageManagerDistributionFile::setType(const std::string &sType) {
    m_sType = sType;
}