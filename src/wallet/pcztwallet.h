// Copyright (c) 2019 The Zcash developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef ZCASH_WALLET_PCZTWALLET_H
#define ZCASH_WALLET_PCZTWALLET_H

#include <pczt.h>
#include <wallet/wallet.h>

enum class TransactionError {
    OK, //!< No error
    MISSING_SPENDING_KEY,
    MISSING_WITNESS,
};

std::string TransactionErrorString(const TransactionError err);

/**
 * Adds an output to PCZT using the wallet.
 */

TransactionError AddOutputPczt(
    CWallet* pwallet,
    Pczt& pczt,
    libzcash::SaplingPaymentAddress& to,
    CAmount value,
    std::array<unsigned char, ZC_MEMO_SIZE> memo = {{0xF6}});

/**
 * Funds a PCZT using the wallet.
 */
TransactionError FundPczt(
    CWallet* pwallet,
    Pczt& pczt,
    libzcash::SaplingPaymentAddress& address);

#endif /* ZCASH_WALLET_PCZTWALLET_H */
