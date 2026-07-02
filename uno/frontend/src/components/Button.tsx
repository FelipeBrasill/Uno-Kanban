interface ButtonProps {
  text: string
  onClick: () => void
}

function Button({ text, onClick }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className="bg-primary text-white font-semibold px-8 py-3 rounded-lg hover:opacity-90 transition"
    >
      {text}
    </button>
  )
}

export default Button