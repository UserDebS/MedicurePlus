export interface OrderItem {
    name: string
    quantity: number
}


interface MedicineData {
    name: string
    cost: number
    available: boolean
    medical_conditions: string[]
    active_ingredients: string[]
    dosage_forms: string[]
    side_effects: string[]
    brand_names: string[]
}

export interface MedicineDetails {
    name: string
    cost: number
    available: boolean
    self_url: string //http://localhost:3000/medicines/{id}
}

export interface MedicineDetailedData {
    data: MedicineData;
    recommendation: MedicineDetails[]
}