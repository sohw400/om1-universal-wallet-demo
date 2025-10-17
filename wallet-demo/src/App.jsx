import { useState } from 'react'
import { useWeb3Modal } from '@web3modal/wagmi/react'
import { useAccount, useSignMessage, useDisconnect, useSwitchChain, useSendTransaction } from 'wagmi'
import { parseEther } from 'viem'

function App() {
  const { open } = useWeb3Modal()
  const { address, isConnected, chain } = useAccount()
  const { signMessage, data: signature } = useSignMessage()
  const { disconnect } = useDisconnect()
  const { switchChain } = useSwitchChain()
  const { sendTransaction, data: txHash } = useSendTransaction()

  const [selectedNetwork, setSelectedNetwork] = useState('1')

  const networks = [
    { id: 1, name: 'Ethereum' },
    { id: 137, name: 'Polygon' },
    { id: 11155111, name: 'Sepolia' }
  ]

  const styles = {
    page: {
      minHeight: '100vh',
      width: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#f5f5f5',
      padding: '20px',
      boxSizing: 'border-box'
    },
    container: {
      width: '100%',
      maxWidth: '600px',
      padding: '40px',
      background: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      boxSizing: 'border-box'
    },
    title: {
      fontSize: '24px',
      marginBottom: '30px',
      textAlign: 'center',
      color: '#333'
    },
    button: {
      width: '100%',
      padding: '14px',
      background: '#1a73e8',
      color: 'white',
      border: 'none',
      borderRadius: '6px',
      fontSize: '16px',
      cursor: 'pointer',
      marginBottom: '12px'
    },
    select: {
      width: '100%',
      padding: '14px',
      background: 'white',
      border: '1px solid #ddd',
      borderRadius: '6px',
      fontSize: '16px',
      cursor: 'pointer',
      marginBottom: '12px'
    },
    info: {
      background: '#f5f5f5',
      padding: '16px',
      borderRadius: '6px',
      marginBottom: '20px',
      fontSize: '14px'
    },
    result: {
      background: '#e8f5e9',
      padding: '12px',
      borderRadius: '6px',
      marginTop: '12px',
      fontSize: '13px',
      wordBreak: 'break-all'
    }
  }

  const handleSign = async () => {
    await signMessage({ message: 'Test signature from OM1 Universal Wallet' })
  }

  const handleNetworkChange = async (e) => {
    const chainId = parseInt(e.target.value)
    setSelectedNetwork(e.target.value)
    await switchChain({ chainId })
  }

  const handleSendTx = async () => {
    try {
      await sendTransaction({
        to: address,
        value: parseEther('0.001')
      })
    } catch (err) {
      console.error('Transaction failed:', err)
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1 style={styles.title}>OM1 Universal Wallet Demo</h1>

        {!isConnected ? (
          <button style={styles.button} onClick={() => open()}>
            Connect Wallet
          </button>
        ) : (
          <>
            <div style={styles.info}>
              <div><strong>Address:</strong> {address?.slice(0, 6)}...{address?.slice(-4)}</div>
              <div><strong>Network:</strong> {chain?.name}</div>
            </div>

            <select style={styles.select} value={selectedNetwork} onChange={handleNetworkChange}>
              {networks.map(net => (
                <option key={net.id} value={net.id}>
                  {net.name}
                </option>
              ))}
            </select>

            <button style={styles.button} onClick={handleSign}>
              Sign Message
            </button>

            <button style={styles.button} onClick={handleSendTx}>
              Send Test Transaction (0.001 ETH to self)
            </button>

            <button style={{...styles.button, background: '#dc3545'}} onClick={() => disconnect()}>
              Disconnect
            </button>

            {signature && (
              <div style={styles.result}>
                <strong>Signature:</strong><br/>
                {signature.slice(0, 30)}...
              </div>
            )}

            {txHash && (
              <div style={styles.result}>
                <strong>Transaction:</strong><br/>
                {txHash.slice(0, 30)}...
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default App
