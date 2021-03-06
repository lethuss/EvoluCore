import os, subprocess, shutil
from multiprocessing import Process, Queue, Value
import time
from functools import reduce
import parse
import xmlParse
from libs.millenium.millenium import db
import traceback
import libs.coreFactory.coreFactory as fac
import numpy as np


class log:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def begin_task(cls, pid, core, message):
        print(cls.HEADER +str(pid)+ cls.ENDC + " | " + cls.BOLD +str(core)+ cls.ENDC + " | " + str(message) +" ...")

    @classmethod
    def end_task(cls, pid, core, message):
        print(cls.HEADER +str(pid)+ cls.ENDC + " | " + cls.BOLD +str(core)+ cls.ENDC + " | " + str(message) +cls.BOLD + " OK!" + cls.ENDC)

    @classmethod
    def exit_message(cls, pid):
        print(cls.HEADER + str(pid) + cls.ENDC + " | - | "+ cls.OKGREEN + "DONE!")

    @classmethod
    def error_message(cls, pid, core, message):
        print(cls.HEADER + str(pid) + cls.ENDC + " | " + cls.BOLD + str(core) + cls.ENDC + " | " + cls.FAIL + str(message))

    @classmethod
    def success(cls, pid, core):
        print(cls.HEADER + str(pid) + cls.ENDC + " | " + cls.BOLD + str(core) + cls.ENDC + " | " + cls.OKGREEN + 'SUCCESS!' + cls.ENDC)



    @classmethod
    def bench_begin_task(cls, pid, core, message):
        print(cls.OKBLUE +str(pid)+ cls.ENDC + " | " + cls.BOLD +str(core)+ cls.ENDC + " | " + str(message) +" ...")

    @classmethod
    def bench_end_task(cls, pid, core, message):
        print(cls.OKBLUE + str(pid) + cls.ENDC + " | " + cls.BOLD + str(core) + cls.ENDC + " | " + str(
            message) + cls.BOLD + " OK!" + cls.ENDC)

    @classmethod
    def bench_error_message(cls, pid, core, message):
        print(cls.OKBLUE + str(pid) + cls.ENDC + " | " + cls.BOLD + str(core) + cls.ENDC + " | " + cls.FAIL + str(
            message))

    @classmethod
    def bench_exit_message(cls, pid):
        print(cls.OKBLUE + str(pid) + cls.ENDC + " | - | " + cls.OKGREEN + "DONE!")

    @classmethod
    def bench_numbers(cls, nums):
        print(cls.WARNING)
        print(nums)
        print(cls.ENDC)

class nourish(Process):

    def __init__(self, rootDir, prefix, referenceDir, population, output, key_start, kernel):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir

        self.__population = population
        self.__key_start = key_start
        self.__output = output
        self.__kernel = kernel

        baseFile = "/home/bcrodrigues/Dropbox/tcc/script/base/qsys/baseOriginal.qsys"
        targetDir = "/home/bcrodrigues/tcc/qsys/"

        self.__qFac = xmlParse.qsysFactory(baseFile, targetDir)

    def _setupFolder(self):
        try:
            if os.path.isdir(self.__workingDir):
                shutil.rmtree(self.__workingDir)
                os.makedirs(self.__workingDir)
            else:
                os.makedirs(self.__workingDir)
        except (OSError, FileNotFoundError):
            if os.path.isdir(self.__workingDir):
                shutil.rmtree(self.__workingDir)
                os.makedirs(self.__workingDir)
            else:
                os.makedirs(self.__workingDir)
            # print('Erro no setup das pastas')
            # exit(1)

    def _populateQsys(self):

        code = subprocess.run(["qsys-generate", "--synthesis=VHDL", self.__rootDir + '/qsys/' + self.__prefix + str(self.actual_idx) + ".qsys", "--output-directory=" + self.__rootDir + '/' + str(
            self.actual_idx)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        if code.returncode != 0:
            raise AssertionError

    def _fixTopDesignName(self):

        with open(self.__workingDir + 'base.qsf', 'r') as f:
            lines = f.readlines()

        for x, line in enumerate(lines):
            if 'TOP_LEVEL_ENTITY' in line:
                lines[x] = 'set_global_assignment -name TOP_LEVEL_ENTITY '+self.__prefix+str(self.actual_idx)+'\n'
            if 'QIP_FILE' in line:
                lines[x] = 'set_global_assignment -name QIP_FILE synthesis/'+self.__prefix+str(self.actual_idx)+'.qip\n'

        with open(self.__workingDir + 'base.qsf', 'w') as f:
            for line in lines:
                f.write(line)

    def _compileQuartus(self):

        code = subprocess.run(["cp", "-a", self.__referenceDir+"quartus/.", self.__workingDir])
        if code.returncode != 0:
            raise Exception('Erro na copia dos arquivos quartus')


        self._fixTopDesignName()

        code = subprocess.run(["quartus_sh", "--flow", "compile", self.__workingDir+"base.qpf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if code.returncode != 0:
            raise Exception('Erro na compilação do quartus')

    def _compileSoftware(self, benchmarks):

        os.makedirs(self.__workingDir+'/software')

        code = subprocess.run(["nios2-bsp", "hal", self.__workingDir+'/software/bsp', self.__rootDir + '/qsys/' + self.__prefix + str(self.actual_idx)+'.sopcinfo', "--script=" + self.__referenceDir+ "/bsp/parameters.tcl"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if code.returncode != 0:
            raise Exception('Erro no BSP')


        for benchmark in benchmarks:

            code = subprocess.run(["nios2-app-generate-makefile", "--bsp-dir="+self.__workingDir+'/software/bsp', "--src-rdir="+self.__referenceDir +"software/"+benchmark+"/", "--app-dir=" + self.__workingDir+'/software/'+benchmark+"/", "--elf-name", "code.elf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if code.returncode != 0:
                raise Exception('Erro no makefile')


            code = subprocess.run(["make", "-C", self.__workingDir+'/software/'+benchmark+'/'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if code.returncode != 0:
                raise Exception('Erro no make')

    def _cleanUp(self):
        try:
            shutil.rmtree(self.__workingDir)
            os.remove(self.__rootDir+'/qsys/q'+str(self.__current['id_core'])+'.qsys')
            os.remove(self.__rootDir+'/qsys/q'+str(self.__current['id_core'])+'.sopcinfo')
        except Exception:
            log.bench_error_message(self.__pid,self.__current['id_core'], "ERROR! \n" + traceback.format_exc())

    def run(self):

        self.__pid = os.getpid()

        for idx, individual in enumerate(self.__population):
            # print(fac.factory.format_core_dict(individual))
            self.actual_idx = idx + self.__key_start

            log.begin_task(self.__pid, str(self.actual_idx), "Got core " + str(self.actual_idx))

            self.__qFac.modifyNios(fac.factory.format_core_dict(individual))
            self.__qFac.writeCurrentQsys('q' + str(self.actual_idx) + '.qsys')
            self.__qFac.resetCurrentQsys()

            self.__workingDir = self.__rootDir + '/' + str(self.actual_idx) + '/'
            self._setupFolder()
            log.end_task(self.__pid, str(self.actual_idx), "QSYS files and folders")

            log.begin_task(self.__pid, str(self.actual_idx), "Compiling QSYS")
            try:
                self._populateQsys()
            except AssertionError:
                self.__output.put((self.actual_idx, -1))
                log.error_message(self.__pid, str(self.actual_idx), "Qsys FAIL")
            else:
                log.end_task(self.__pid, str(self.actual_idx), "Compiling QSYS")

                log.begin_task(self.__pid, str(self.actual_idx), "Compiling Quartus Project")
                self._compileQuartus()
                log.end_task(self.__pid, str(self.actual_idx), "Compiling Quartus Project")

                log.begin_task(self.__pid, str(self.actual_idx), "Compiling Software")
                self._compileSoftware(self.__kernel)
                log.end_task(self.__pid, str(self.actual_idx), "Compiling Software")
                #

                log.success(self.__pid, str(self.actual_idx))

                self.__output.put((self.actual_idx, individual))

            #
            #     except Exception:
            #         log.error_message(self.__pid, str(self.__current['id_core']), "ERROR! \n" + traceback.format_exc())

        # self.__db.give_back(self.__current['id_core'])
        # self._cleanUp()
        log.exit_message(self.__pid)

class colosseum(Process):

    def __init__(self, rootDir, prefix, referenceDir, cable, input, result, cleanUp, kernel, fpga_metrics):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir
        self.__cable = cable
        self.__cleanUp =cleanUp
        self.__result = result
        self.__input = input
        self.__running = Value('d', 1)
        self.__kernel = kernel
        self.__fpga_metrics = fpga_metrics


    def _configureBoard(self):

        success = False
        while not success:

            p = subprocess.Popen("quartus_pgm -c "+str(self.__cable) + " -z --mode=JTAG --operation=\"p;" + self.__workingDir +"output_files/base_time_limited.sof@2\"",stdout=subprocess.PIPE, shell=True)

            for line in iter(p.stdout.readline, b''):
                string = line.decode("utf-8")

                if "Configuration succeeded" in string:
                    success = True
                    subprocess.run(["kill", str(p.pid)])
                    break

                if "Operation failed" in string:
                    subprocess.run(["kill", str(p.pid)])
                    subprocess.run(["killall", "jtagd"])
                    break

                if 'does not exist or can\'t be read' in string:
                    raise FileNotFoundError

    def _transferCode(self, benchmark):

        confiredProperly = False
        while not confiredProperly:
            returnCode = -1
            retry = -1

            while returnCode != 0:
                code = subprocess.run(["nios2-download", "-c", str(self.__cable), "-r", "-g", self.__workingDir + "/software/"+benchmark+"/code.elf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                returnCode = code.returncode
                retry += 1
                if retry >= 1:
                    break

            if returnCode != 0:

                subprocess.run(["killall", "jtagd"])
                self._configureBoard()

            else:
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                confiredProperly = True

    def _benchmark(self, benchmark):

        retry = 3

        while True:

            p = subprocess.Popen('nios2-terminal -c '+str(self.__cable)+' -o 4', stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)
            aux = []
            for x in range(10):
                for line in iter(p.stdout.readline, b''):
                    try:
                        string = line.decode("utf-8")
                        aux.append(int(string))
                    except:
                        pass
                    else:
                        break
            try:
                result = reduce(lambda x, y: x + y, aux[4:]) / len(aux[4:])
                log.bench_numbers(aux+[result])
            except:
                if retry > 0:
                    subprocess.run(["nios2-download", "-r", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL)
                    subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    # subprocess.run(["kill", str(p.pid)])
                    retry -= 1
                else:
                    subprocess.run(["kill", str(p.pid)])
                    self._configureBoard()
                    self._transferCode(benchmark)
                    retry = 3
            else:
                subprocess.run(["kill", str(p.pid)])
                return result, aux

    def _getUsageData(self):

        with open(self.__workingDir + "output_files/base.fit.summary", 'r') as f:

            format_string_memory = 'Total block memory bits : {} / {} ( {} % )'
            format_string_ram = 'Total RAM Blocks : {} / {} ( {} % )'
            format_string_alm = 'Logic utilization (in ALMs) : {} / {} ( {} % )'

            output = f.read().splitlines()

            result = []

            for line in output:
                if 'ALMs' in line:
                    parsed = parse.parse(format_string_alm, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    if 'alm' in self.__fpga_metrics:
                        result.append(used)

                if 'block memory bits' in line:
                    parsed = parse.parse(format_string_memory, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    if 'memory' in self.__fpga_metrics:
                        result.append(used)

                if 'Total RAM Blocks' in line:
                    parsed = parse.parse(format_string_ram, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    if 'ram' in self.__fpga_metrics:
                        result.append(used)

            return result

    def _cleanUp(self):
        try:
            shutil.rmtree(self.__workingDir)
            os.remove(self.__rootDir+'/qsys/q'+self.actual_idx+'.qsys')
            os.remove(self.__rootDir+'/qsys/q'+self.actual_idx+'.sopcinfo')
        except Exception:
            log.bench_error_message(self.__pid, self.actual_idx, "ERROR! \n" + traceback.format_exc())

    def shutdown(self):
        self.__running.value = 0

    def run(self):
        self.__pid = os.getpid()
        while self.__running.value:
            try:
                self.__current = self.__input.get_nowait()
            except Exception:
                time.sleep(1)
            else:
                print(self.__current)
                if self.__current[1] == -1:
                    self.__result.put((self.__current[0], -1))
                else:

                    self.actual_idx = str(self.__current[0])

                    log.bench_begin_task(self.__pid, self.actual_idx, "Got core " + self.actual_idx)
                    self.__workingDir = self.__rootDir + '/' + self.actual_idx + '/'

                    try:
                        log.bench_begin_task(self.__pid, self.actual_idx, "Configuring Board")
                        self._configureBoard()
                        log.bench_end_task(self.__pid, self.actual_idx, "Configuring Board")
                    except FileNotFoundError:
                        log.error_message(self.__pid, self.actual_idx, "ERROR! Invalid Core")
                        self.__result.put((self.__current[1]), -1)
                    except Exception:
                        log.bench_error_message(self.__pid, self.__current, "ERROR! \n" + traceback.format_exc())
                    else:

                        log.bench_begin_task(self.__pid, self.actual_idx, "Fetching FPGA usage data")
                        result = self._getUsageData()
                        # result['id'] = int(self.actual_idx)
                        log.bench_end_task(self.__pid, self.actual_idx, "Fetching FPGA usage data")

                        log.bench_begin_task(self.__pid, self.actual_idx, "Benchmarking")
                        for benchmark in self.__kernel:

                            aux = []

                            log.bench_begin_task(self.__pid, self.actual_idx, "Transfering "+ benchmark)
                            self._transferCode(benchmark)
                            log.bench_end_task(self.__pid, self.actual_idx, "Transfering "+ benchmark)

                            log.bench_begin_task(self.__pid, self.actual_idx, "Getting results from " + benchmark)
                            media, times = self._benchmark(benchmark)
                            log.bench_end_task(self.__pid, self.actual_idx, "Getting results from " + benchmark)

                            aux.append(media)

                            result = aux + result

                        # print((self.__current[1], tuple(result)))
                        self.__result.put((self.__current[1], tuple(result)))

                        if self.__cleanUp:
                            self._cleanUp()
                            log.bench_end_task(self.__pid, self.actual_idx, "Cleaning up ")

                    log.bench_end_task(self.__pid,  self.actual_idx, "Benchmarking")

        log.bench_exit_message(self.__pid)

class Generator(Process):

    def __init__(self, rootDir, toCompile, prefix, referenceDir, toBenchmark):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__toCompile = toCompile
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir
        self.__toBenchmark = toBenchmark

    def _setupFolder(self):
        try:
            if os.path.isdir(self.__workingDir):
                shutil.rmtree(self.__workingDir)
                os.makedirs(self.__workingDir)
            else:
                os.makedirs(self.__workingDir)
        except OSError:
            print('Erro no setup das pastas')
            exit(1)

    def _populateQsys(self):

        code = subprocess.run(["qsys-generate --synthesis=VHDL "+ self.__rootDir + '/qsys/' + self.__prefix + self.__current + ".qsys --output-directory=" + self.__rootDir + '/' + self.__current], shell=True)
        if code.returncode != 0:
            print('Erro na compilação do Qsys')
            raise AssertionError

    def _fixTopDesignName(self):

        with open(self.__workingDir + 'base.qsf', 'r') as f:
            lines = f.readlines()

        for x, line in enumerate(lines):
            if 'TOP_LEVEL_ENTITY' in line:
                lines[x] = 'set_global_assignment -name TOP_LEVEL_ENTITY '+self.__prefix+self.__current+'\n'
            if 'QIP_FILE' in line:
                lines[x] = 'set_global_assignment -name QIP_FILE synthesis/'+self.__prefix+self.__current+'.qip\n'

        with open(self.__workingDir + 'base.qsf', 'w') as f:
            for line in lines:
                f.write(line)

    def _compileQuartus(self):

        code = subprocess.run(["cp", "-a", self.__referenceDir+"quartus/.", self.__workingDir])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        self._fixTopDesignName()

        code = subprocess.run(["quartus_sh", "--flow", "compile", self.__workingDir+"base.qpf"])
        if code.returncode != 0:
            print('Erro na compilação do quartus')
            exit()

    def _compileSoftware(self, benchmarks):

        os.makedirs(self.__workingDir+'/software')

        code = subprocess.run(["nios2-bsp", "hal", self.__workingDir+'/software/bsp', self.__rootDir + '/qsys/' + self.__prefix + self.__current+'.sopcinfo', "--script=" + self.__referenceDir+ "/bsp/parameters.tcl"])
        if code.returncode != 0:
            print('Erro na copia dos arquivos quartus')
            exit()

        for benchmark in benchmarks:

            code = subprocess.run(["nios2-app-generate-makefile", "--bsp-dir="+self.__workingDir+'/software/bsp', "--src-rdir="+self.__referenceDir +"software/"+benchmark+"/", "--app-dir=" + self.__workingDir+'/software/'+benchmark+"/", "--elf-name", "code.elf"])
            if code.returncode != 0:
                print('Erro na copia dos arquivos quartus')
                exit()

            code = subprocess.run(["make", "-C", self.__workingDir+'/software/'+benchmark+'/'])
            if code.returncode != 0:
                print('Erro na copia dos arquivos quartus')
                exit()

    def run(self):

        self.__pid = os.getpid()

        while True:
            try:
                self.__current = str(self.__toCompile.get_nowait())
            except Exception:
                exit(0)
            else:
                print(str(self.__pid) + " " +self.__current)
                self.__workingDir = self.__rootDir +'/'+self.__current+'/'
                self._setupFolder()
                try:
                    self._populateQsys()
                except AssertionError:
                    self.__toBenchmark.put(int(self.__current))
                else:
                    self._compileQuartus()
                    self._compileSoftware(['sobel'])
                    self.__toBenchmark.put(int(self.__current))

class Generator_on_db(Process):

    def __init__(self, rootDir, prefix, referenceDir, toBenchmark, running):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir
        self.__toBenchmark = toBenchmark
        self.__running =running

        baseFile = "/home/bcrodrigues/Dropbox/tcc/script/base/qsys/baseOriginal.qsys"
        targetDir = "/home/bcrodrigues/tcc/qsys/"

        self.__qFac = xmlParse.qsysFactory(baseFile, targetDir)

        self.__db = db()

    def _setupFolder(self):
        try:
            if os.path.isdir(self.__workingDir):
                shutil.rmtree(self.__workingDir)
                os.makedirs(self.__workingDir)
            else:
                os.makedirs(self.__workingDir)
        except OSError:
            print('Erro no setup das pastas')
            exit(1)

    def _populateQsys(self):

        code = subprocess.run(["qsys-generate", "--synthesis=VHDL", self.__rootDir + '/qsys/' + self.__prefix + str(
            self.__current['id_core']) + ".qsys", "--output-directory=" + self.__rootDir + '/' + str(
            self.__current['id_core'])], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        if code.returncode != 0:
            raise AssertionError

    def _fixTopDesignName(self):

        with open(self.__workingDir + 'base.qsf', 'r') as f:
            lines = f.readlines()

        for x, line in enumerate(lines):
            if 'TOP_LEVEL_ENTITY' in line:
                lines[x] = 'set_global_assignment -name TOP_LEVEL_ENTITY '+self.__prefix+str(self.__current['id_core'])+'\n'
            if 'QIP_FILE' in line:
                lines[x] = 'set_global_assignment -name QIP_FILE synthesis/'+self.__prefix+str(self.__current['id_core'])+'.qip\n'

        with open(self.__workingDir + 'base.qsf', 'w') as f:
            for line in lines:
                f.write(line)

    def _compileQuartus(self):

        code = subprocess.run(["cp", "-a", self.__referenceDir+"quartus/.", self.__workingDir])
        if code.returncode != 0:
            raise Exception('Erro na copia dos arquivos quartus')


        self._fixTopDesignName()

        code = subprocess.run(["quartus_sh", "--flow", "compile", self.__workingDir+"base.qpf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if code.returncode != 0:
            raise Exception('Erro na compilação do quartus')

    def _compileSoftware(self, benchmarks):

        os.makedirs(self.__workingDir+'/software')

        code = subprocess.run(["nios2-bsp", "hal", self.__workingDir+'/software/bsp', self.__rootDir + '/qsys/' + self.__prefix + str(self.__current['id_core'])+'.sopcinfo', "--script=" + self.__referenceDir+ "/bsp/parameters.tcl"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if code.returncode != 0:
            raise Exception('Erro no BSP')


        for benchmark in benchmarks:

            code = subprocess.run(["nios2-app-generate-makefile", "--bsp-dir="+self.__workingDir+'/software/bsp', "--src-rdir="+self.__referenceDir +"software/"+benchmark+"/", "--app-dir=" + self.__workingDir+'/software/'+benchmark+"/", "--elf-name", "code.elf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if code.returncode != 0:
                raise Exception('Erro no makefile')


            code = subprocess.run(["make", "-C", self.__workingDir+'/software/'+benchmark+'/'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if code.returncode != 0:
                raise Exception('Erro no make')

    def _cleanUp(self):
        try:
            shutil.rmtree(self.__workingDir)
            os.remove(self.__rootDir+'/qsys/q'+str(self.__current['id_core'])+'.qsys')
            os.remove(self.__rootDir+'/qsys/q'+str(self.__current['id_core'])+'.sopcinfo')
        except Exception:
            log.bench_error_message(self.__pid,self.__current['id_core'], "ERROR! \n" + traceback.format_exc())

    def run(self):

        self.__pid = os.getpid()
        while self.__running.value:
            self.__current = self.__db.get_free_core()
            if self.__current == None:
                log.exit_message(self.__pid)
                exit(0)
            else:
                try:

                    log.begin_task(self.__pid, str(self.__current['id_core']), "Got core " + str(self.__current['id_core']))
                    self.__qFac.modifyNios(self.__current)
                    self.__qFac.writeCurrentQsys('q' + str(self.__current['id_core']) + '.qsys')
                    self.__qFac.resetCurrentQsys()
                    self.__workingDir = self.__rootDir + '/' + str(self.__current['id_core']) + '/'
                    self._setupFolder()
                    log.end_task(self.__pid, str(self.__current['id_core']), "QSYS files and folders")

                    if not self.__running.value:
                        break

                    log.begin_task(self.__pid, str(self.__current['id_core']), "Compiling QSYS")
                    self._populateQsys()
                    log.end_task(self.__pid, str(self.__current['id_core']), "Compiling QSYS")

                    if not self.__running.value:
                        break

                    log.begin_task(self.__pid, str(self.__current['id_core']), "Compiling Quartus Project")
                    self._compileQuartus()
                    log.end_task(self.__pid, str(self.__current['id_core']), "Compiling Quartus Project")

                    if not self.__running.value:
                        break

                    log.begin_task(self.__pid, str(self.__current['id_core']), "Compiling Software")
                    self._compileSoftware(['sobel', 'quicksort', 'adpcm', 'dotprod', 'vecsum'])
                    log.end_task(self.__pid, str(self.__current['id_core']), "Compiling Software")

                    self.__db.get_core_ready_to_bench(self.__current['id_core'])
                    log.success(self.__pid, str(self.__current['id_core']))

                except Exception:
                    log.error_message(self.__pid, str(self.__current['id_core']), "ERROR! \n" + traceback.format_exc())

        self.__db.give_back(self.__current['id_core'])
        self._cleanUp()
        log.exit_message(self.__pid)

class TestBench(Process):

    def __init__(self, rootDir, prefix, referenceDir, cable, result, cleanUp, running):

        Process.__init__(self)
        self.__rootDir = rootDir
        self.__workingDir = rootDir
        self.__current = None
        self.__pid = None
        self.__prefix = prefix
        self.__referenceDir = referenceDir
        self.__cable = cable
        self.__cleanUp =cleanUp
        self.__result = result
        self.__running =running
        self.__db = db()

    def _configureBoard(self):

        success = False
        while not success:

            p = subprocess.Popen("quartus_pgm -c "+str(self.__cable) + " -z --mode=JTAG --operation=\"p;" + self.__workingDir +"output_files/base_time_limited.sof@2\"",stdout=subprocess.PIPE, shell=True)

            for line in iter(p.stdout.readline, b''):
                string = line.decode("utf-8")

                if "Configuration succeeded" in string:
                    success = True
                    subprocess.run(["kill", str(p.pid)])
                    break

                if "Operation failed" in string:
                    subprocess.run(["kill", str(p.pid)])
                    subprocess.run(["killall", "jtagd"])
                    break

                if 'does not exist or can\'t be read' in string:
                    raise FileNotFoundError

    def _transferCode(self, benchmark):

        confiredProperly = False
        while not confiredProperly:
            returnCode = -1
            retry = -1

            while returnCode != 0:
                code = subprocess.run(["nios2-download", "-c", str(self.__cable), "-r", "-g", self.__workingDir + "/software/"+benchmark+"/code.elf"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                returnCode = code.returncode
                retry += 1
                if retry > 5:
                    break

            if returnCode != 0:
                subprocess.run(["killall", "jtagd"])
                self._configureBoard()
            else:
                subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                confiredProperly = True

    def _benchmark(self, benchmark):

        retry = 3

        while True:

            p = subprocess.Popen('nios2-terminal -c '+str(self.__cable)+' -o 4', stdout=subprocess.PIPE, preexec_fn=os.setsid, shell=True)
            aux = []
            for x in range(10):
                for line in iter(p.stdout.readline, b''):
                    try:
                        string = line.decode("utf-8")
                        aux.append(int(string))
                    except:
                        pass
                    else:
                        break
            try:
                result = reduce(lambda x, y: x + y, aux[4:]) / len(aux[4:])
                log.bench_numbers(aux+[result])
            except:
                if retry > 0:
                    subprocess.run(["nios2-download", "-r", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL,
                                   stdout=subprocess.DEVNULL)
                    subprocess.run(["nios2-download", "-c", str(self.__cable), "-g"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    # subprocess.run(["kill", str(p.pid)])
                    retry -= 1
                else:
                    subprocess.run(["kill", str(p.pid)])
                    self._configureBoard()
                    self._transferCode(benchmark)
                    retry = 3
            else:
                subprocess.run(["kill", str(p.pid)])
                return result, aux

    def _getUsageData(self):

        with open(self.__workingDir + "output_files/base.fit.summary", 'r') as f:

            format_string_memory = 'Total block memory bits : {} / {} ( {} % )'
            format_string_ram = 'Total RAM Blocks : {} / {} ( {} % )'
            format_string_alm = 'Logic utilization (in ALMs) : {} / {} ( {} % )'

            output = f.read().splitlines()

            result = {}

            for line in output:
                if 'ALMs' in line:
                    parsed = parse.parse(format_string_alm, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    result['alm'] = used

                if 'block memory bits' in line:
                    parsed = parse.parse(format_string_memory, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    result['memory'] = used

                if 'Total RAM Blocks' in line:
                    parsed = parse.parse(format_string_ram, line)

                    used = int(parsed[0].replace(',', ''))
                    total = int(parsed[1].replace(',', ''))

                    result['ram'] = used

            return result

    def _cleanUp(self):
        try:
            shutil.rmtree(self.__workingDir)
            os.remove(self.__rootDir+'/qsys/q'+self.__current+'.qsys')
            os.remove(self.__rootDir+'/qsys/q'+self.__current+'.sopcinfo')
        except Exception:
            log.bench_error_message(self.__pid, self.__current, "ERROR! \n" + traceback.format_exc())

    def run(self):

        self.__pid = os.getpid()
        while self.__running.value:
            try:
                # self.__current = str(self.__toBenchmark.get_nowait())
                self.__current = str(self.__db.get_benchable_core()['id_core'])
            except Exception:
                time.sleep(1)
            else:

                log.bench_begin_task(self.__pid, self.__current, "Got core " + str(self.__current))

                self.__workingDir = self.__rootDir + '/' + self.__current + '/'
                try:
                    log.bench_begin_task(self.__pid, self.__current, "Configuring Board")
                    self._configureBoard()
                    log.bench_end_task(self.__pid, self.__current, "Configuring Board")
                except FileNotFoundError:
                    log.error_message(self.__pid, str(self.__current), "ERROR! Invalid Core")
                    self.__db.invalidate_core(int(self.__current))

                except Exception:
                    log.bench_error_message(self.__pid, self.__current, "ERROR! \n" + traceback.format_exc())
                else:

                    log.bench_begin_task(self.__pid, self.__current, "Fetching FPGA usage data")
                    result = self._getUsageData()
                    result['id'] = int(self.__current)
                    log.bench_end_task(self.__pid, self.__current, "Fetching FPGA usage data")

                    log.bench_begin_task(self.__pid, self.__current, "Benchmarking")
                    for benchmark in ['sobel', 'quicksort', 'adpcm', 'dotprod', 'vecsum']:

                        aux= {}

                        log.bench_begin_task(self.__pid, self.__current, "Transfering "+ benchmark)
                        self._transferCode(benchmark)
                        log.bench_end_task(self.__pid, self.__current, "Transfering "+ benchmark)

                        log.bench_begin_task(self.__pid, self.__current, "Getting results from " + benchmark)
                        media, times = self._benchmark(benchmark)
                        log.bench_end_task(self.__pid, self.__current, "Getting results from " + benchmark)

                        aux['time'] = media
                        aux['times'] = times

                        result[benchmark] = aux

                    if self.__cleanUp:
                        self._cleanUp()
                        log.bench_end_task(self.__pid, self.__current, "Cleaning up ")

                    log.bench_end_task(self.__pid, self.__current, "Benchmarking")
                    self.__db.insert_results(result)

        log.bench_exit_message(self.__pid)

class nature():

    def __init__(self, kernel, fpga):

        self.target = "/home/bcrodrigues/tcc/"
        self.base = "/home/bcrodrigues/Dropbox/tcc/script/base/"
        self.result = Queue()
        self.interface = Queue()
        self.prefix = 'q'
        self.kernel = kernel
        self.fpga = fpga

    def life(self, population):

        # print('Population in nature:', population)

        step = int(population.shape[0]/4)

        # print(step, len(population[0:step]), len(population[step:step*2]), len(population[step*2:step*3]), len(population[step*3:]))

        gen1 = nourish(self.target, self.prefix, self.base, population[0:step], self.interface, 0, self.kernel)
        gen2 = nourish(self.target, self.prefix, self.base, population[step:step*2], self.interface, step, self.kernel)
        gen3 = nourish(self.target, self.prefix, self.base, population[step*2:step*3], self.interface,step*2, self.kernel)
        gen4 = nourish(self.target, self.prefix, self.base, population[step*3:], self.interface, step*3, self.kernel)

        gen1.start()
        gen2.start()
        gen3.start()
        gen4.start()

        arena1 = colosseum(self.target, self.prefix, self.base, 1, self.interface, self.result, False, self.kernel, self.fpga)
        # arena2 = colosseum(self.target, self.prefix, self.base, 2, self.interface, self.result,  True, self.kernel)

        arena1.start()
        # arena2.start()


        traits = []
        objectives = []

        while len(traits) < population.shape[0]:
            aux = self.result.get()
            if aux[1] != -1:
                traits.append(aux[0])
                objectives.append(aux[1])
            else:
                core = fac.factory.generate_random_cores(1)
                gen_aux = nourish(self.target, self.prefix, self.base, core, self.interface, aux[0], self.kernel)
                gen_aux.start()




        arena1.shutdown()
        # arena2.shutdown()

        return np.array(traits), np.array(objectives)






if __name__ == '__main__':

    import libs.coreFactory.coreFactory as fac

    cores = fac.factory.generate_random_cores(4)
    # print(cores)

    natur = nature(['adpcm'], ['alm'])

    natur.life(cores)