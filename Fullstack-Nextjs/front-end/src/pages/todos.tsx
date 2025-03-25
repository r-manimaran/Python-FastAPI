import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getTodos, deleteTodo, updateStatus } from "@/lib/api";
import { Todo } from "@/types/types";
import CreateTodoForm from "@/components/createTodoForm";

export default function TodosPage() {

    const queryClient = useQueryClient();

    const { data: todos, isLoading, error}=useQuery({
        queryKey: ["todos"],
        queryFn: getTodos,
    });

     // Mutation for deleting a todo
  const deleteMutation = useMutation({
    mutationFn: deleteTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] }); // Refresh the todo list
    },
  });

  // Mutation for update complete status
  const completeMutation = useMutation({
    mutationFn: updateStatus,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] }); // Refresh the todo list
    },
  });
  

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div className="max-w-2xl mx-auto p-6">
          <h1 className="text-2xl font-bold text-center mb-4">Todo List</h1>

            <CreateTodoForm />

          {/* <ul className="space-y-4">
            {todos?.map((todo: Todo) => (
              <li
                key={todo.id}
                className="p-4 border rounded-lg shadow-md bg-white"
              >
                <h2 className="text-xl font-semibold">{todo.title}</h2>
                <p className="text-gray-600">{todo.description}</p>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    todo.complete ? "bg-green-500 text-white" : "bg-red-500 text-white"
                  }`}
                >
                  {todo.complete ? "Completed" : "Pending"}
                </span>
              </li>
            ))}
          </ul> */}
          <ul className="mt-6 space-y-4">
        {todos?.map((todo: Todo) => (
          <li key={todo.id} className="p-4 border rounded-lg shadow-md bg-white flex justify-between items-center">
            <div>
              <h2 className="text-xl font-semibold">{todo.title}</h2>
              <p className="text-gray-600">{todo.description}</p>
              <span
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  todo.complete ? "bg-green-500 text-white" : "bg-red-500 text-white"
                }`}
              >
                {todo.complete ? "Completed" : "Pending"}
              </span>
            </div>
            <div className="space-x-2">
              {
                !todo.complete && (
                  <button 
                  onClick={()=> completeMutation.mutate(todo.id)}
                  className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                  disabled={completeMutation.isPending}
                  >
                    {completeMutation.isPending ? "Completing..." : "Complete"}
                  </button>
                )
              }
            

            <button
              onClick={() => deleteMutation.mutate(todo.id)}
              className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? "Deleting..." : "Delete"}
            </button>
            </div>
          </li>
        ))}
      </ul>
        </div>
      );
}
