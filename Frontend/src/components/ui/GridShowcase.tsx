import { useEffect } from "react";

const GridShowcase = ({
    children,
    setOffset
} : {
    children : React.ReactNode,
    setOffset : React.Dispatch<React.SetStateAction<number>>
}) => {

    useEffect(() => {
        const scroller = document.getElementById('gridscroller');

        let debounceTimeout: NodeJS.Timeout;
        const handleScroll = () => {
            clearTimeout(debounceTimeout);
            debounceTimeout = setTimeout(() => {
                if (scroller) {
                    const { scrollTop, scrollHeight, clientHeight } = scroller;
                    if (scrollTop + clientHeight >= scrollHeight - 1) {
                        setOffset((prev) => prev + 20);
                    }
                }
            }, 1000);
        };

        scroller?.addEventListener('scroll', handleScroll);

        return () => {
            scroller?.removeEventListener('scroll', handleScroll);
            clearTimeout(debounceTimeout); // Clear timeout on cleanup
        };
    }, []);

    return ( 
        <section id="gridscroller" className={`w-full h-full flex justify-center items-start gap-1 overflow-x-hidden overflow-y-scroll flex-wrap p-2`}>
            {children}
        </section>
     );
}
 
export default GridShowcase;