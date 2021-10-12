<template>
  <div class="flex justify-between items-center py-4 bg-green-500">
    <div class="flex-shrink-0 ml-10 cursor-default">
      <span class="ml-1 text-3xl text-white font-semibold">Sistema de gestión de pedidos</span>
    </div>
    <ul class="hidden md:flex overflow-x-hidden mr-10 font-semibold">
      <li class="mr-6 p-1 border-b-2 border-orange-500">
        <a class="text-white cursor-default" href="#">Inicio</a>
      </li>
      <li class="mr-6 p-1">
        <a
          class="text-white hover:text-green-300"
          href="#"
          >Intranet</a
        >
      </li>
      <li class="mr-6 p-1">
        <a class="text-white hover:text-green-300" href="#"
          >Cambiar de modulo</a
        >
      </li>
      <li class="mr-6 p-1">
        <a
          class="text-white hover:text-green-300"
          href="#"
          >Cerrar sesión</a
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Header"
};
</script>
