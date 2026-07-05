import Benyo from '../assets/players/benyo.png'
import Calvo from '../assets/players/calvo.jpeg'
import Reali from '../assets/players/realiehgay.jpeg'
import McLovin from '../assets/players/mclovin.jpeg'

import { Carta, CartaVirada } from '../components/Carta'
import ContainerPlayer from '../components/ContainerPlayer'
import MaoPlayer from '../components/MaoPlayer'

function Partida() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100">
      <div className="flex flex-col w-[90vw] h-[87vh] gap-2 rounded-lg p-8 items-center justify-between">
        <div className="flex flex-row items-center justify-between w-full h-2/5 rounded-lg p-0">
            {/* Comprar carta */}
            <div className="flex flex-col items-center justify-start h-full w-1/3 rounded-lg p-0 cursor-pointer"
                onClick={()=>{alert("Carta Comprada")}}
            >
                <span className="text-2xl font-bold">Comprar Carta</span>
                <CartaVirada />
            </div>    
            
            {/* Benyo */}
            <div className="flex flex-col items-center justify-start h-full w-1/3 rounded-lg p-0">
                <ContainerPlayer playerImage={Benyo} playerName="Benyo" Orientation="top" />
                <MaoPlayer rotation={180}>
                    <CartaVirada />
                </MaoPlayer>
            </div>
            
            
            <div className="w-1/3"></div>
        </div>
        <div className="flex flex-row items-center justify-between h-1/5 w-2/3 rounded-lg p-4">
            
            {/* Calvo */}
            <div className="flex flex-row items-center justify-start gap-2">
                <ContainerPlayer playerImage={Calvo} playerName="Calvo" Orientation="left" />
                <MaoPlayer rotation={90}>
                    <CartaVirada />
                </MaoPlayer>
            </div>

            {/* Carta Central */}
            
            <Carta rotate={45} />
            {/* McLovin */}
            <div className="flex flex-row items-center justify-end gap-2">
                <MaoPlayer rotation={270}>
                    <CartaVirada />
                </MaoPlayer>
                <ContainerPlayer playerImage={McLovin} playerName="McLovin" Orientation="right" />
            </div>
        </div>
        {/* Reali */}
        <div className="flex flex-col items-center justify-end h-2/5 rounded-lg p-0 gap-2">
            <MaoPlayer rotation={0}>
                    <Carta valor='+40' />
                </MaoPlayer>
            <ContainerPlayer playerImage={Reali} playerName="O Gay" Orientation="bottom" />
        </div>
      </div>
    </div>
  )
}

export default Partida