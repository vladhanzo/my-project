// frontend/src/components/ModelConfigurator.tsx
import { useEffect, useState } from "react"
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  IconButton,
} from "@mui/material"
import { Add, Delete, Edit } from "@mui/icons-material"
import axios from "axios"

interface RequiredComponent {
  id: number
  name: string
  quantity: number
  isCritical: boolean
}

const defaultComponent: Omit<RequiredComponent, "id"> = {
  name: "",
  quantity: 1,
  isCritical: false,
}

export default function ModelConfigurator() {
  const [components, setComponents] = useState<RequiredComponent[]>([])
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editId, setEditId] = useState<number | null>(null)
  const [form, setForm] = useState<Omit<RequiredComponent, "id">>(defaultComponent)

  useEffect(() => {
    axios.get("/api/components/required").then((res) => setComponents(res.data))
  }, [])

  const handleSubmit = async () => {
    if (form.quantity < 1) return
    try {
      if (editId === null) {
        const res = await axios.post("/api/components/required", form)
        setComponents((prev) => [...prev, res.data])
      } else {
        const res = await axios.put(`/api/components/required/${editId}`, form)
        setComponents((prev) =>
          prev.map((c) => (c.id === editId ? res.data : c)),
        )
      }
      setForm(defaultComponent)
      setEditId(null)
      setDialogOpen(false)
    } catch {}
  }

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`/api/components/required/${id}`)
      setComponents((prev) => prev.filter((c) => c.id !== id))
    } catch {}
  }

  const handleEdit = (component: RequiredComponent) => {
    setForm({ name: component.name, quantity: component.quantity, isCritical: component.isCritical })
    setEditId(component.id)
    setDialogOpen(true)
  }

  return (
    <>
      <Button onClick={() => setDialogOpen(true)} startIcon={<Add />}>
        Add Component
      </Button>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Critical</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {components.map((c) => (
            <TableRow key={c.id}>
              <TableCell>{c.name}</TableCell>
              <TableCell>{c.quantity}</TableCell>
              <TableCell>{c.isCritical ? "Yes" : "No"}</TableCell>
              <TableCell>
                <IconButton onClick={() => handleEdit(c)}><Edit /></IconButton>
                <IconButton onClick={() => handleDelete(c.id)}><Delete /></IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>{editId === null ? "Add" : "Edit"} Component</DialogTitle>
        <DialogContent>
          <TextField
            label="Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Quantity"
            type="number"
            value={form.quantity}
            onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value, 10) || 1 })}
            fullWidth
            margin="normal"
          />
          <Checkbox
            checked={form.isCritical}
            onChange={(e) => setForm({ ...form, isCritical: e.target.checked })}
          /> Critical
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSubmit}>Save</Button>
        </DialogActions>
      </Dialog>
    </>
  )
}
