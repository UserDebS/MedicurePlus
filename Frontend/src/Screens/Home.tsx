import Med_Card from "@/components/ui/Card";
import apiFetcher from "@/lib/apiFetcher";
import { MedicineDetails } from "@/lib/datatypes";
import { useEffect, useState } from "react";

const Home = () => {
    const [medList, setMedList] = useState<MedicineDetails[]>();
    const fetchData = async() => {
        await apiFetcher.getAllMedicines(0, 30).then(async(res) =>  {
            const data = await res.json();
            setMedList(data);
        }).catch(_ => console.log(_));
    }
    useEffect(() => {
        fetchData();
    }, [])
    return ( 
        <div className="h-full w-full flex justify-center items-center flex-wrap gap-2">
            {
                medList?.map(data => <Med_Card 
                    name={data.name} 
                    cost={data.cost}
                    available={data.available}
                    self_url={data.self_url}
                />)
            }
        </div>
     );
}
 
export default Home;