import Benyo from '../assets/players/benyo.png'
import Calvo from '../assets/players/calvo.jpeg'
import Reali from '../assets/players/realiehgay.jpeg'
import McLovin from '../assets/players/mclovin.jpeg'

function ConteinerPlayer({ playerImage, playerName }: { playerImage: string, playerName: string}) {
    return (
        <div className="flex flex-col items-center justify-center gap-4 rounded-lg p-4">
            <img src={playerImage} alt={playerName} className="w-16 h-16 rounded-full object-cover" />
            <h1 className="text-xl font-bold">{playerName}</h1>
        </div>
    )
}

function CartaVirada() {
    return (
        <div className="flex w-18 h-28 bg-black rounded-lg shadow-lg p-1 border-2 border-primary items-center justify-center">
                <h1 className="text-white text-[18px] font-bold rotate-45">KABUNO</h1>
        </div>
    )
}

function Partida() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100">
      <div className="flex flex-col bg-red-400 w-[90vw] h-[85vh] gap-2 rounded-lg shadow-lg p-8">
        <div className="flex flex-col items-center justify-start h-2/5 bg-blue-400 rounded-lg shadow-lg p-4 gap-2">
            <ConteinerPlayer playerImage={Benyo} playerName="Benyo" />
            <CartaVirada />
        </div>
        <div className="flex flex-row items-center justify-between h-1/5 bg-green-400 rounded-lg shadow-lg p-4">
            <div className="flex flex-row items-center justify-start gap-2">
                <ConteinerPlayer playerImage={Calvo} playerName="Calvo" />
                <CartaVirada />
            </div>
            <div className="flex flex-row items-center justify-end gap-2">
                <CartaVirada />
                <ConteinerPlayer playerImage={McLovin} playerName="McLovin" />
            </div>
        </div>
        <div className="flex flex-col items-center justify-end h-2/5 bg-yellow-400 rounded-lg shadow-lg p-4 gap-2">
            <CartaVirada />
            <ConteinerPlayer playerImage={Reali} playerName="O Gay" />
        </div>
      </div>
    </div>
  )
}

export default Partida