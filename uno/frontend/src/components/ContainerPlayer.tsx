function ContainerPlayerImg({ playerImage, playerName }: { playerImage: string, playerName: string }) {
    return (
        <div className="flex flex-col items-center justify-center gap-0 rounded-lg p-1">
            <img src={playerImage} alt={playerName} className="w-12 h-12 rounded-full object-cover" />
            <span className="text-lg font-bold">{playerName}</span>
        </div>
    )
}

function ContainerPlayerScore({ score }: { score: number }) {
    return (
        <div className="flex flex-row bg-purple-500 gap-4 rounded-lg p-4">
            <h1 className="text-xl font-bold">{score}</h1>
        </div>
    )
}

type Orientation = "left" | "right" | "top" | "bottom"

interface ContainerPlayerProps {
    playerImage: string
    playerName: string
    Orientation: Orientation
    score?: number
}

function ContainerPlayer({ playerImage, playerName, Orientation: orientation, score=0 }: ContainerPlayerProps) {

    const isImageFirst = orientation === "right" || orientation === "bottom"
    const align = orientation === "left" || orientation === "top" ? "justify-start" : "justify-end"
    const flexDirection = orientation === "left" || orientation === "right" ? "flex-row" : "flex-col"

    const image = <ContainerPlayerImg playerImage={playerImage} playerName={playerName} />
    const scoreElement = <ContainerPlayerScore score={score} />
    
    return (
        <div className={`flex ${flexDirection} items-center ${align} gap-1 rounded-lg p-4 h-[65%] `}>
            {
                isImageFirst ? (
                    <>
                        {image}
                        {scoreElement}
                    </>
                ) : (
                    <>
                        {scoreElement}
                        {image}
                    </>
                )
            }
        </div>
    );
}

export default ContainerPlayer