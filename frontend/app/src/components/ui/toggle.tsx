type ToggleProps = {
    isActive: boolean;
    onToggle: () => void;
  };
  
  const Toggle: React.FC<ToggleProps> = ({ isActive, onToggle }) => {
    return (
      <span className="block">
        <button 
          type="button"
          onClick={onToggle}
          className={`relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:shadow-outline ${isActive ? 'bg-primary' : 'bg-gray-300'}`}
          aria-label="Toggle"
          role="switch"
        >
          <span className={`inline-block h-5 w-5 rounded-full bg-white shadow transform transition ease-in-out duration-200 ${isActive ? 'translate-x-5' : 'translate-x-0'}`}></span>
        </button>
      </span>
    );
  };
  
  export default Toggle;
  