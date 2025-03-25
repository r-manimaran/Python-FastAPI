'use client';
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { createTodo } from "@/lib/api";

const todoSchema = z.object({
  title: z.string().min(3,"Title must be at least 3 characters."),
  description: z.string().min(10,"Description must be at least 10 characters"),
  priority: z.number().min(1).max(5),
});

type TodoFormData = z.infer<typeof todoSchema>;

export default function CreateTodoForm() {
    const {
        register,
        handleSubmit,
        formState: {errors},
        reset
    }= useForm<TodoFormData>({
        resolver: zodResolver(todoSchema),
    });

    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: createTodo,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["todos"] }); // Refresh Todo List
            reset(); // clear the form
        },
    });

    const onSubmit = (data: TodoFormData) => {
        mutation.mutate({...data, complete: false});
    };

   
        return (
            <div className="max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md">
              <h2 className="text-xl font-bold mb-4">Create a New Todo</h2>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label className="block font-medium">Title</label>
                  <input
                    type="text"
                    {...register("title")}
                    className="w-full p-2 border rounded"
                  />
                  {errors.title && <p className="text-red-500 text-sm">{errors.title.message}</p>}
                </div>
        
                <div>
                  <label className="block font-medium">Description</label>
                  <textarea
                    {...register("description")}
                    className="w-full p-2 border rounded"
                  ></textarea>
                  {errors.description && <p className="text-red-500 text-sm">{errors.description.message}</p>}
                </div>
        
                <div>
                  <label className="block font-medium">Priority (1-5)</label>
                  <input
                    type="number"
                    {...register("priority", { valueAsNumber: true })}
                    className="w-full p-2 border rounded"
                  />
                  {errors.priority && <p className="text-red-500 text-sm">{errors.priority.message}</p>}
                </div>
        
                <button
                  type="submit"
                  className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
                  disabled={mutation.isPending}
                >
                  {mutation.isPending ? "Creating..." : "Create Todo"}
                </button>
              </form>
            </div>
          );
    








}