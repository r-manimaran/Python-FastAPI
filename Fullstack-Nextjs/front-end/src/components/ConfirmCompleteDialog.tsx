import { AlertDialog, AlertDialogTrigger, 
        AlertDialogContent, AlertDialogHeader, 
        AlertDialogTitle, AlertDialogDescription,
        AlertDialogFooter, AlertDialogCancel, 
        AlertDialogAction } from "@/components/ui/alert-dialog";

interface ConfirmCompleteDialogProps {
  onConfirm: () => void;
}

export default function ConfirmCompleteDialog({ onConfirm }: ConfirmCompleteDialogProps) {
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <button className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600">
          Complete
        </button>
      </AlertDialogTrigger>

      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Confirm Completion</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to mark this task as complete? You cannot undo this action.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={onConfirm} className="bg-green-500 hover:bg-green-600">
            Confirm
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
